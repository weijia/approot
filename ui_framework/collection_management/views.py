# Create your views here.

from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from django.conf import settings

'''
[
        {
            

            
        "data": "title",//required field
                "attr": { "url": "view://tags",
                          "id": "xxx-ssss-xxxxx--xxxxxx", //id must not contain char ":"
                        },
                "state": "closed"
        }
]
'''


from django.core import serializers
from ui_framework.objsys.models import UfsObj, CollectionItem

    
def collections(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
        
        
    json_serializer = serializers.get_serializer("json")()
    
    response =  json_serializer.serialize(UfsObj.objects.all(), ensure_ascii=False, indent=2, use_natural_keys=True)
    return HttpResponse(response, mimetype="application/json")
    
    '''
    c = {"user": request.user, "tree": {"name": "left_tree", "url":"hello"}}
    c.update(csrf(request))
    return render_to_response('objsys/manager.html', c)
    '''
'''
def getCollectionByProtocol(collectionId, dbSysInst):
    moduleName, itemUrl = collectionId.split("://",2)
    collectionModule = __import__("libs.collections.modules."+moduleName, globals(),locals(),["getCollection"], -1)
    return collectionModule.getCollection(itemUrl, dbSysInst)
'''
def collections_jstree(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    parent_uuid = request.REQUEST["node"]
    
    root_uuid = "4a5e8673-f2a2-4cf2-af6c-461fa9f31a15"
    
    if parent_uuid == '-1':
        parent_uuid = root_uuid
    
    parent_list = []
    
    anonymous_user = User.objects.filter(pk=settings.ANONYMOUS_USER_ID)[0]
    
    for i in CollectionItem.objects.filter(uuid=parent_uuid):
        #Scan all child for this parent to check if the child is a parent (so it can be expanded)
        if 0 != CollectionItem.objects.filter(uuid = i.obj.uuid).count():
            #There is at least one child for this item
            parent_list.append(i.obj.uuid)
        #Check if there is a dynamic child, id_in_col will contain
        #"dynamic://" if it is an item with dynamic children
        # Only one dynmaic child is considered. So we redirect directly when met a dynamic child.
        if u"dynamic://" in i.id_in_col:
            #return resolve(request.REQUEST["node"].replace("view://","/"))(request) 
            return redirect(i.id_in_col.replace(u"dynamic://",u"/"))
        
        
    c = {"user": request.user, "collections": CollectionItem.objects.filter(uuid=parent_uuid),
            "parent_list": parent_list, "default_user": anonymous_user}

    c.update(csrf(request))
    return render_to_response('collection_management/collection_in_json.json', c, mimetype="application/json")

