from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from tagging.models import TaggedItem
from utils.django_utils import retrieve_param


__author__ = 'Administrator'


def get_tag_info_for_obj(obj):
    ctype = ContentType.objects.get_for_model(obj)
    obj_pk = obj.pk
    tagged_item_list = TaggedItem.objects.filter(content_type=ctype, object_id=obj.pk)
    res = []
    for tagged_item in tagged_item_list:
        res.append({"tag": tagged_item.tag.name, "app": tagged_item.tag_app})
    return res


def handle_export_tags(request):
    data = retrieve_param(request)
    try:
        from object_filter.operations_local import ExportTagsThread
    except ImportError:
        return HttpResponse('{"result": "Not supported here"}', mimetype="application/json")
    t = ExportTagsThread()
    t.set_data(data)
    #t.set_tag_app('user:' + request.user.username)
    t.start()
    return HttpResponse('{"result": "Apply tags processing"}', mimetype="application/json")