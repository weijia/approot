import json
import logging

from django.contrib.auth.models import User
from django.views.generic import TemplateView
from tagging.models import Tag
from webmanager.default_user_conf import get_default_username_and_pass

from objsys.models import UfsObj, Description
from objsys.tastypie_related.tastypie_import import TastypieItem
from config.conf_storage import ConfStorage
from ufs_utils.django_utils import retrieve_param
from ufs_utils.obj_tools import is_web_url
from ufs_utils.web.smart_opener import open_url
from ufs_utils.web.url_updater import update_url_param, get_server_base
from ufs_diagram.django_processor_state import DjangoProcessorState


log = logging.getLogger(__name__)


class ObjExportTask(TemplateView):
    template_name = "url_based_task_apps/export_result.html"
    #TASK_UFS_URL = "task://export_from_localhost"
    #DIAGRAM_UFS_URL = "diagram://load_from_localhost"
    NEXT_URL_PARAM_NAME = "next_url"
    DEFAULT_PROCESSOR_UUID = "invalid_processor_uuid"

    @staticmethod
    def get_default_initial_import_url():
        default_admin_user, default_admin_password = get_default_username_and_pass()
        return "http://" + ConfStorage.get_ufs_server_and_port_str() + \
               "/objsys/api/ufsobj/ufsobj/?" + \
               "format=json&username=%s&password=%s" % (default_admin_user, default_admin_password)

    #noinspection PyAttributeOutsideInit
    def get_context_data(self, **kwargs):
        #return super(TaskResultView, self).get_context_data(**kwargs)
        context_data = super(ObjExportTask, self).get_context_data(**kwargs)
        #log.error(context_data)
        data = retrieve_param(self.request)
        #log.error(data)
        #print context_data
        dict_result = {}
        self.result = ""
        #self.server_base = data.get("server_base", "http://" + ConfStorage.get_ufs_server_and_port_str())
        self.process_uuid = data.get("process_uuid", self.DEFAULT_PROCESSOR_UUID)
        self.initial_import_url = data.get("initial_import_url", self.get_default_initial_import_url())
        self.server_base = get_server_base(self.initial_import_url)

        self.state_storage = DjangoProcessorState(self.process_uuid)
        self.processor_state = self.state_storage.get_state()
        log.debug(str(self.processor_state))

        #log.error(self.processor_state)
        next_url = self.get_next_url(self.processor_state)
        #log.error(next_url)
        dict_result = self.fetch_json_data(next_url)
        if self.is_new_obj_received(dict_result):
            #log.error("is updated returns true")
            self.save_data_to_file(dict_result)
            self.save_next_url(dict_result)
        return {"result": self.result}

    def get_saved_attr_value(self, state_attr, default_value=0):
        if state_attr in self.processor_state:
            saved_attr_value = self.processor_state[state_attr]
        else:
            saved_attr_value = default_value
        return saved_attr_value

    def is_new_obj_received(self, dict_result):
        #print dict_result["meta"]
        saved_total_count = self.get_saved_attr_value("total_count")
        saved_offset = self.get_saved_attr_value("offset")
        saved_limit = self.get_saved_attr_value("limit")
        if saved_offset + saved_limit > saved_total_count:
            if dict_result["meta"]["total_count"] == saved_total_count:
                return False
        return True

    def get_next_url(self, state):
        if self.NEXT_URL_PARAM_NAME in state:
            next_url = state[self.NEXT_URL_PARAM_NAME]
        else:
            next_url = self.initial_import_url
        return next_url

    def update_new_state_for_attr(self, retrieved_data_dict, state_attr):
        if state_attr in retrieved_data_dict["meta"]:
            self.new_state[state_attr] = retrieved_data_dict["meta"][state_attr]
            self.result += state_attr + ":" + str(retrieved_data_dict["meta"][state_attr]) + "\n"

    def save_next_url(self, retrieved_data_dict):
        self.new_state = self.processor_state.copy()
        #log.error(retrieved_data_dict)
        #log.error(""+str(self.new_state))
        if "meta" in retrieved_data_dict:
            if ("next" in retrieved_data_dict["meta"]) and \
                    (not (retrieved_data_dict["meta"]["next"] is None)):
                self.result += "saving next:" + retrieved_data_dict["meta"]["next"] + "\n"

                self.new_state[self.NEXT_URL_PARAM_NAME] = self.server_base + retrieved_data_dict["meta"]["next"]
            elif self.NEXT_URL_PARAM_NAME in self.new_state:
                if is_web_url(self.new_state[self.NEXT_URL_PARAM_NAME]):
                    self.new_state[self.NEXT_URL_PARAM_NAME] = \
                        update_url_param(self.new_state[self.NEXT_URL_PARAM_NAME], "offset",
                                         retrieved_data_dict["meta"]["total_count"])
                    self.new_state["real_offset"] = retrieved_data_dict["meta"]["total_count"]
                else:
                    del self.new_state[self.NEXT_URL_PARAM_NAME]

            self.update_new_state_for_attr(retrieved_data_dict, "total_count")
            self.update_new_state_for_attr(retrieved_data_dict, "offset")
            self.update_new_state_for_attr(retrieved_data_dict, "limit")

            #log.error("saving new state: "+str(self.new_state))
            self.state_storage.save_state(self.new_state)

    @staticmethod
    def fetch_json_data(data_url):
        response = open_url(data_url)
        result = json.loads(response.read())
        return result

    def import_one_obj(self, item):
        tastypie_item = TastypieItem(item)
        if tastypie_item.is_valid_url() and (0 == UfsObj.objects.filter(ufs_url=tastypie_item.get_url()).count()):
            user_id = self.kwargs['user_id']
            user = User.objects.get(pk=user_id)
            tags_str = tastypie_item.get_tag_str()
            del item["tags"]
            description = tastypie_item.get_description_content()

            del item["descriptions"]
            del item["resource_uri"]
            del item["id"]
            obj = UfsObj(user=user, **item)
            obj.save()
            if description != "":
                description_obj, created = Description.objects.get_or_create(content=description)
                obj.descriptions.add(description_obj)
                obj.save()
            Tag.objects.update_tags(obj, tags_str, tag_app='import from BAE')
            self.result += "Tag:" + tags_str + "\n\n"
        else:
            self.result += "ignored:" + tastypie_item.get_url() + "\nis valid:" + str(
                tastypie_item.is_valid_url()) + "\n"

    def import_data_from_tastypie_result(self, decoded):
        #decoded = json.loads(result)
        for item in decoded["objects"]:
            #tastypie_item = TastypieItem(item)
            self.import_one_obj(item)

    def save_data_to_file(self, dict_result):
        path = ConfStorage.get_server_exporting_free_name(self.server_base)
        of = open(path, "w")
        json.dump(dict_result, of, indent=4)
        of.close()