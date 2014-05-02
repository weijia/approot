import json
from django.http import HttpResponse
from objsys.models import UfsObj
from ufs_utils.django_utils import retrieve_param


class ObjOperator(object):
    def __init__(self, pk):
        self.pk = pk

    def rm(self):
        for obj in UfsObj.objects.filter(pk=self.pk):
            invalid_obj_and_rm_tags(obj)


class ObjListOperator(object):
    def __init__(self, obj_list):
        self.obj_list = obj_list

    def rm(self):
        for obj in self.obj_list:
            invalid_obj_and_rm_tags(obj)


def invalid_obj_and_rm_tags(obj):
    json_description = obj.description_json
    if not (json_description is None):
        description_dict = json.loads(json_description)
        description_dict["tags_before_delete"] = obj.tags
        obj.description_json = description_dict.dumps(description_dict)
    obj.tags = ""
    obj.valid = False
    obj.save()


def get_obj_from_data(data):
    if "pk" in data:
        return UfsObj.objects.filter(pk=data["pk"])
    if "ufs_url" in data:
        return UfsObj.objects.filter(ufs_url=data["ufs_url"])


def handle_operation_request(request):
    data = retrieve_param(request)
    json_result_str = '{"result": "not enough params"}'
    if "cmd" in data:
        operator = ObjListOperator(get_obj_from_data(data))
        getattr(operator, data["cmd"])()
        json_result_str = '{"result": "removed: %s"}' % (data["ufs_url"])
    return HttpResponse(json_result_str, mimetype="application/json")


def rm_obj_from_db(request):
    data = retrieve_param(request)
    json_result_str = '{"result": "not enough params"}'
    if "ufs_url" in data:
        for obj in UfsObj.objects.filter(ufs_url=data["ufs_url"]):
            invalid_obj_and_rm_tags(obj)
        json_result_str = '{"result": "removed: %s"}' % (data["ufs_url"])
    return HttpResponse(json_result_str, mimetype="application/json")