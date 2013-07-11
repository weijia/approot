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



def filesystem_rest(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    res = []
    parent = string_tools.unquote_unicode(data["full_path"])
    for filename in os.listdir(parent):
        full_path = os.path.join(parent, filename)
        res.append({"full_path": full_path, "description": full_path, "tags": []})
    response = json.dumps({"objects": res, "meta": {"next": ""}}, sort_keys=True, indent=4)
    return HttpResponse(response, mimetype="application/json")