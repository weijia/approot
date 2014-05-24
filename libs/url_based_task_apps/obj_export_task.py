import json
import logging
import urllib2
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from tagging.models import Tag
from connection.models import Processor
from objsys.models import UfsObj, Description
from objsys.tastypie_import import TastypieItem
from config.conf_storage import ConfStorage
from ufs_utils.django_utils import retrieve_param


log = logging.getLogger(__name__)


class ObjExportTask(TemplateView):
    template_name = "url_based_task_apps/export_result.html"
    TASK_UFS_URL = "task://export_from_localhost"
    SERVER_BASE = "http://127.0.0.1:8110"
    INITIAL_IMPORT_URL = SERVER_BASE + "/objsys/api/ufsobj/ufsobj/?" \
                                       "format=json&username=richard&password=johnpassword"
    DIAGRAM_UFS_URL = "diagram://load_from_baidu"
    NEXT_URL_PARAM_NAME = "next_url"

    def get_context_data(self, **kwargs):
        #return super(TaskResultView, self).get_context_data(**kwargs)
        context_data = super(ObjExportTask, self).get_context_data(**kwargs)
        #log.error(context_data)
        data = retrieve_param(self.request)
        #log.error(data)
        #print context_data
        dict_result = {}
        self.result = ""
        process_ufs_url = data.get("process_ufs_url", self.TASK_UFS_URL)
        diagram_ufs_url = data.get("diagram_ufs_url", self.DIAGRAM_UFS_URL)

        self.processor_state = self.load_task_state(process_ufs_url, diagram_ufs_url)
        next_url = self.get_next_url(self.processor_state)
        dict_result = self.fetch_json_data(next_url)
        if self.is_updated(dict_result):
            self.save_data_to_file(dict_result)
            self.save_next_url(dict_result)
        return {"result": self.result}

    def is_updated(self, dict_result):
        if ("meta" in dict_result) and ("total_count" in dict_result["meta"]):
            total_count = dict_result["meta"]["total_count"]
            if "total_count" in self.processor_state:
                saved_total_count = self.processor_state["total_count"]
            else:
                saved_total_count = 0
            if total_count != saved_total_count:
                return True
        self.result += "item not updated "
        return False

    def get_next_url(self, state):
        if "next_url" in state:
            next_url = state[self.NEXT_URL_PARAM_NAME]
        else:
            next_url = self.INITIAL_IMPORT_URL
        return next_url

    def save_next_url(self, result):
        state = {}
        if "meta" in result:
            if ("next" in result["meta"]) and \
                    (not (result["meta"]["next"] is None)):
                self.result += "saving next:" + result["meta"]["next"]

                state[self.NEXT_URL_PARAM_NAME] = self.SERVER_BASE + result["meta"]["next"]
            if "total_count" in result["meta"]:
                state["total_count"] = result["meta"]["total_count"]
                self.result += "total_count:" + str(result["meta"]["total_count"])
            log.error(state)
            self.save_task_state(state)

    def load_task_state(self, process_ufs_url, diagram_ufs_url):
        task_obj, created = UfsObj.objects.get_or_create(ufs_url=process_ufs_url)
        diagram_obj, created = UfsObj.objects.get_or_create(ufs_url=diagram_ufs_url)
        processor, created = Processor.objects.get_or_create(ufsobj=task_obj, diagram_obj=diagram_obj)
        result = {}
        if (not (processor.param_descriptor is None)) and (not (processor.param_descriptor == "")):
            result = json.loads(processor.param_descriptor)
        self.result += str(result)
        return result

    @staticmethod
    def fetch_json_data(data_url):
        response = urllib2.urlopen(data_url)
        result = json.loads(response.read())
        return result

    def save_task_state(self, state):
        task_obj = UfsObj.objects.get(ufs_url=self.TASK_UFS_URL)
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

    @staticmethod
    def save_data_to_file(dict_result):
        path = ConfStorage.get_free_name_for_exported_data()
        of = open(path, "w")
        json.dump(dict_result, of, indent=4)
        of.close()