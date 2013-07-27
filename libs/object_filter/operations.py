import json
import os
import threading
import time
from libs.tagging.models import TaggedItem
from libs.utils.objTools import getHostName
import libsys
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from libs.utils.django_utils import retrieve_param
from ui_framework.objsys.views import ApplyTagsThread, UfsFilter
from django.contrib.contenttypes.models import ContentType
from libs.utils.misc import ensureDir as ensure_dir


__author__ = 'Administrator'


def get_tag_info_for_obj(obj):
    ctype = ContentType.objects.get_for_model(obj)
    obj_pk = obj.pk
    tagged_item_list = TaggedItem.objects.filter(content_type=ctype, object_id=obj.pk)
    res = []
    for tagged_item in tagged_item_list:
        res.append({"tag": tagged_item.tag.name, "app": tagged_item.tag_app})
    return res


def export_json_to_folder(final_data, relative_path):
    root_dir = libsys.get_root_dir()
    dump_root = os.path.join(root_dir, relative_path)
    ensure_dir(dump_root)
    dump_filename = os.path.join(root_dir, relative_path + str(time.time()) + ".json")
    f = open(dump_filename, "w")
    f.write(json.dumps(final_data, indent=4))
    f.close()


class ExportTagsThread(UfsFilter, threading.Thread):
    def run(self):
        final_data = []
        for obj in self.get_obj_filters():
            final_data.append({"tags": get_tag_info_for_obj(obj), "ufs_url": obj.ufs_url,
                               "uuid": obj.uuid, "full_path": obj.full_path,
                               "description": obj.description, "size": obj.size})
        ######
        # Quitting, so save last_timestamp
        if 0 != len(final_data):
            export_json_to_folder({"data": final_data, "host": getHostName()}, "../tag_dump/")
        else:
            print "No more tag applied"


def handle_export_tags(request):
    data = retrieve_param(request)
    t = ExportTagsThread()
    t.set_data(data)
    #t.set_tag_app('user:' + request.user.username)
    t.start()
    return HttpResponse('{"result": "Apply tags processing"}', mimetype="application/json")
