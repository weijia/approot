from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from tagging.models import Tag, TaggedItem
#from django.core import serializers
from ui_framework.objsys.models import UfsObj, CollectionItem
import json

# Create your views here.
def object_filter(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    if data.has_key("tag"):
        c = {"user": request.user, "tag": data["tag"], "filter_tag": True}
    else:
        c = {"user": request.user}
    c.update(csrf(request))
    return render_to_response('object_filter/index.html', c)