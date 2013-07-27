from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from tagging.models import Tag, TaggedItem
#from django.core import serializers
from ui_framework.objsys.models import UfsObj, CollectionItem
import json
import libs.utils.string_tools as string_tools
from operations import *


# Create your views here.
def object_filter(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    c = {"user": request.user}
    if "tag" in data:
        c["tag"] = data["tag"]
        c["filter_tag"] = True

    if "query_base" in data:
        c["query_base"] = string_tools.unquote_unicode(data["query_base"])
        c["query_base_exists"] = True

    c.update(csrf(request))
    return render_to_response('object_filter/index.html', c)


def object_table(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST

    c = {"user": request.user}
    '''
    if "tag" in data:
        c["tag"] = data["tag"]
        c["filter_tag"] = True

    if "query_base" in data:
        c["query_base"] = string_tools.unquote_unicode(data["query_base"])
        c["query_base_exists"] = True
    '''
    c.update(csrf(request))
    return render_to_response('object_filter/table.html', c)