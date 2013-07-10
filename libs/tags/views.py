# Create your views here.

from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from tagging.models import Tag, TaggedItem
#from django.core import serializers
from ui_framework.objsys.models import UfsObj, CollectionItem
import json

def tag_list(request):
    """
    Generate tag list in the system with tagged item's count.
    :param request:
    :return: the returned data is in JSON:
    [{"data": "private(10)", "attr": {"url": "/object_filter/?tag=private"}}]
    """
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
        
        
    #json_serializer = serializers.get_serializer("json")()
    
    tags = Tag.objects.usage_for_model(UfsObj, counts=True)
    
    res = []
    for tag in tags:
        res.append({"data": "%s(%d)"%(tag.name, tag.count), "attr" : {"url": "/object_filter/?tag=%s"%tag.name}})
    
    #response =  json_serializer.serialize(res, ensure_ascii=False, indent=2, use_natural_keys=True)
    response = json.dumps(res, sort_keys=True, indent=4)    
    return HttpResponse(response, mimetype="application/json")

    
def list_tagged(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
        
        
    if data.has_key("tag"):
        tag = data["tag"]
        
    from tagging.models import Tag
    obj_tag = Tag.objects.get(name=tag)
    objs = TaggedItem.objects.get_by_model(UfsObj, obj_tag)

    res = []
    for obj in objs:
        res.append({"data": obj.ufs_url, "full_path": obj.full_path})
    
    #response =  json_serializer.serialize(res, ensure_ascii=False, indent=2, use_natural_keys=True)
    response = json.dumps(res, sort_keys=True, indent=4)    
    return HttpResponse(response, mimetype="application/json")

    
    
def pane(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    if data.has_key("tag"):
        tag = data["tag"]
        data_url = "/tags/tagged/?tag="+tag
    else:
        data_url = "/tags/"
    c = {"user": request.user, "data_url": data_url}
    c.update(csrf(request))
    return render_to_response('tags/pane.html', c)
