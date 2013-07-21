from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
import os
from tagging.models import Tag, TaggedItem
#from django.core import serializers
from ui_framework.objsys.models import UfsObj, CollectionItem
import json
import libsys
from libs.windows.windowsDriver import getDriverList
import urllib2
import libs.utils.string_tools as string_tools


def root(request):
    """
    Generate root folder list
    :param request:
    :return:
    [{"data": "D:/", "attr": {"url": "/filemanager/listdir?path=D:/"}}]
    For supporting object_filter view, we added another structure:
    {"full_path":"D:/", "description": "..."}
    """
    driver_list = getDriverList()
    res = []
    for driver in driver_list:
        res.append({"data": driver,
                    "attr":
                        {"url": "/object_filter?query_base=" +
                                string_tools.quote_unicode(u"/filemanager/filesystem_rest/?full_path=") + driver,
                         "id": string_tools.quote_unicode(u"local_filesystem://" + driver)
                        },
                    "state": "closed"
        })
    response = json.dumps(res, sort_keys=True, indent=4)
    return HttpResponse(response, mimetype="application/json")


def root_rest(request):
    """
    Used for content display
    Generate root folder list in rest api format as generated Tastypie
    :param request:
    :return:
    For supporting object_filter view, we added another structure:
    {"full_path":"D:/", "description": "..."}
    """
    driver_list = getDriverList()
    res = []
    for driver in driver_list:
        res.append({"full_path": driver, "description": "Driver", "tags": [], "object_name": driver
        })
    response = json.dumps({"objects": res, "meta": {"next": ""}}, sort_keys=True, indent=4)
    return HttpResponse(response, mimetype="application/json")


import libs.utils.transform as transform
import libs.utils.objTools as obj_tools

gDefaultFileListCnt = 20


def filesystem_rest(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    res = []
    parent = string_tools.unquote_unicode(data["full_path"])
    offset = 0
    if "offset" in data:
        offset = int(data["offset"])
    end_cnt = offset + gDefaultFileListCnt
    is_in_range = False
    cnt = 0
    for filename in os.listdir(parent):
        if cnt >= offset:
            is_in_range = True
        cnt += 1
        if not is_in_range:
            continue
        if cnt > end_cnt:
            break
        full_path = os.path.join(parent, filename)
        full_path = transform.transformDirToInternal(full_path)
        tags = []
        for obj in UfsObj.objects.filter(full_path=full_path):
            for tag in obj.tags:
                tags.append(tag.name)
        res.append(
            {"ufs_url": obj_tools.getUfsUrl(full_path), "full_path": full_path, "description": full_path, "tags": tags})

    response = json.dumps(
        {"objects": res, "meta":
            {"next": request.path + "?full_path=" + string_tools.quote_unicode(parent) +
                     "&limit=20&offset=%d&format=json" % end_cnt}
        }, sort_keys=True, indent=4)
    return HttpResponse(response, mimetype="application/json")