import json
import logging
import urllib2
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from tagging.models import Tag
from connection.models import Processor
from objsys.models import UfsObj, Description
from objsys.tastypie_related.tastypie_import import TastypieItem
from config.conf_storage import ConfStorage
from ufs_utils.django_utils import retrieve_param
from webmanager.default_user_conf import get_default_username_and_pass


log = logging.getLogger(__name__)


class ObjExportTask(TemplateView):
    template_name = "url_based_task_apps/export_result.html"
    TASK_UFS_URL = "task://export_from_localhost"
    DIAGRAM_UFS_URL = "diagram://load_from_localhost"
    NEXT_URL_PARAM_NAME = "next_url"


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
        self.server_base = data.get("server_base", "http://" + ConfStorage.get_ufs_server_and_port_str())
        self.process_ufs_url = data.get("process_ufs_url", self.TASK_UFS_URL)
        self.diagram_ufs_url = data.get("diagram_ufs_url", self.DIAGRAM_UFS_URL)
        self.initial_import_url = data.get("initial_import_url", self.get_default_initial_import_url())
        self.force_direct_access_param = data.get("force_direct_access", "yes")

        if self.force_direct_access_param == "yes":
            self.force_direct_access = True
        else:
            self.force_direct_access = False

        self.processor_state = self.load_task_state()
        #log.error(self.processor_state)
        next_url = self.get_next_url(self.processor_state)
        #log.error(next_url)
        dict_result = self.fetch_json_data(next_url)
        if self.is_updated(dict_result):
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

    def is_updated(self, dict_result):
        saved_total_count = self.get_saved_attr_value("total_count")
        saved_offset = self.get_saved_attr_value("offset")
        saved_limit = self.get_saved_attr_value("limit")
        if saved_offset + saved_limit > saved_total_count:
            if dict_result["meta"]["total_count"] == saved_total_count:
                return False
        return True

    def get_next_url(self, state):
        if "next_url" in state:
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
        self.new_state[self.NEXT_URL_PARAM_NAME] = self.get_saved_attr_value(self.NEXT_URL_PARAM_NAME)
        #log.error(retrieved_data_dict)
        if "meta" in retrieved_data_dict:
            if ("next" in retrieved_data_dict["meta"]) and \
                    (not (retrieved_data_dict["meta"]["next"] is None)):
                self.result += "saving next:" + retrieved_data_dict["meta"]["next"] + "\n"

                self.new_state[self.NEXT_URL_PARAM_NAME] = self.server_base + retrieved_data_dict["meta"]["next"]

            self.update_new_state_for_attr(retrieved_data_dict, "total_count")
            self.update_new_state_for_attr(retrieved_data_dict, "offset")
            self.update_new_state_for_attr(retrieved_data_dict, "limit")

            #log.error("saving new state: "+str(self.new_state))
            self.save_task_state(self.new_state)

    def load_task_state(self):
        task_obj, created = UfsObj.objects.get_or_create(ufs_url=self.process_ufs_url)
        diagram_obj, created = UfsObj.objects.get_or_create(ufs_url=self.diagram_ufs_url)
        processor, created = Processor.objects.get_or_create(ufsobj=task_obj, diagram_obj=diagram_obj)
        result = {}
        if (not (processor.param_descriptor is None)) and (not (processor.param_descriptor == "")):
            result = json.loads(processor.param_descriptor)
        self.result += str(result)
        return result

    def fetch_json_data(self, data_url):
        if not self.force_direct_access:
            response = urllib2.urlopen(data_url)
        else:
            proxy_handler = urllib2.ProxyHandler({})
            opener = urllib2.build_opener(proxy_handler)
            response = opener.open(data_url)
        result = json.loads(response.read())
        return result

    def save_task_state(self, state):
        task_obj = UfsObj.objects.get(ufs_url=self.process_ufs_url)
        processor = Processor.objects.get(ufsobj=task_obj)
        self.result += "processor:" + str(processor) + "\n"
        processor.param_descriptor = json.dumps(state)
        processor.save()
        self.result += "saved:" + str(processor.param_descriptor) + "\n"

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
        encoded_server = self.server_base.replace("http://", "").replace("/", "_").replace(":", "_") + "_"
        path = ConfStorage.get_free_name_for_exported_data(encoded_server)
        of = open(path, "w")
        json.dump(dict_result, of, indent=4)
        of.close()