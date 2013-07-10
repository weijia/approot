from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from tagging.models import Tag, TaggedItem
#from django.core import serializers
from ui_framework.objsys.models import UfsObj, CollectionItem
import json
import libsys
from libs.windows.windowsDriver import getDriverList


def root(request):
    """
    Generate root folder list
    :param request:
    :return:
    [{"data": "D:/", "attr": {"url": "/filemanager/listdir?path=D:/"}}]
    """
    driver_list = getDriverList()
    res = []
    for driver in driver_list:
        res.append({"data": driver + "/", "attr": {"url": "/filemanager/listdir/path=" + driver +"/"}})
    response = json.dumps(res, sort_keys=True, indent=4)
    return HttpResponse(response, mimetype="application/json")

