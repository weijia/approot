# Create your views here.
#from django.template import Context, loader
#from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
import os
from models import UfsObj
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from libs.services.svc_base.gui_service import GuiService
import libsys
from libs.utils.string_tools import SpecialEncoder
import libs.utils.objTools as objtools
from tagging.models import Tag, TaggedItem
import json


@login_required
def tagging(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    
    #Load saved url
    if request.session.has_key("saved_urls"):
        stored_urls = request.session["saved_urls"]
    else:
        stored_urls = []
    selected_url = []
    urls = []
    close_flag = False
    if data.has_key("encoding"):
        encoding = data["encoding"]
    else:
        encoding = "utf8"
    
    if data.has_key("tags"):
        tags = data["tags"]
    else:
        tags = []
    #print tags
    decoder = SpecialEncoder()
            
    for query_param_list in data.lists():
        if query_param_list[0] == "url":
            allurls = []
            for url in query_param_list[1]:
                allurls.append(decoder.decode(url))
            stored_urls.extend(allurls)
            for url in stored_urls:
                if not (url in urls):
                    #print query_param_list, urls
                    urls.append(url)
        if query_param_list[0] == 'selected_url':
            close_flag = True
            for url in query_param_list[1]:
                if not (url in selected_url):
                    selected_url.append(url)
                    #Tag object
                    '''
                    try:
                        objs = UfsObj.objects.filter(ufs_url = url)
                        if 0 != len(objs):
                            for obj in objs:
                                obj.tags = tags
                            continue
                    except UfsObj.DoesNotExist:
                        pass
                    '''
                    
                    full_path = objtools.get_full_path_for_local_os(url)
                    obj_qs = UfsObj.objects.filter(full_path = full_path)
                    
                    if 0 != obj_qs.count():
                        for obj in obj_qs:
                            #obj.tags = tags
                            Tag.objects.update_tags(obj, tags, tag_app = 'user:'+request.user.username)
                        continue
                    #print "Create new item"
                    import uuid
                    from django.utils import timezone
                    ufs_url = objtools.getUfsUrlForPath(full_path)
                    obj = UfsObj(ufs_url = ufs_url, uuid = unicode(uuid.uuid4()), timestamp=timezone.now(), user = request.user, full_path = full_path)
                    obj.save()
                    #obj.tags = tags
                    Tag.objects.update_tags(obj, tags, tag_app = 'user:'+request.user.username)
    class UrlTagPair:
        def __init__(self, url, tags):
            self.url = url
            self.tags = tags
                        
                    
    request.session["saved_urls"] = urls
    urls_with_tags = []
    for url in urls:
        tags = []
        full_path = objtools.get_full_path_for_local_os(url)
        obj_qs = UfsObj.objects.filter(full_path = full_path)
        print obj_qs.count()
        if 0 != obj_qs.count():
            print 'object exists'
            for obj in obj_qs:
                print obj.tags
                tags.extend(obj.tags)
        urls_with_tags.append(UrlTagPair(url, tags))
    
    c = {"urls": urls, "user": request.user, "close_flag": close_flag, "urls_with_tags": urls_with_tags}
    c.update(csrf(request))
    return render_to_response('objsys/tagging.html', c)

    
    
def manager(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    c = {"user": request.user, "tree": {"name": "left_tree", "url":"/collection_management/jstree/?node="}}
    c.update(csrf(request))
    return render_to_response('objsys/manager.html', c)

    
def query(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    c = {"user": request.user}
    c.update(csrf(request))
    return render_to_response('objsys/query.html', c)

import threading

class StarterThread(threading.Thread):
    def __init__(self, path):
        super(StarterThread, self).__init__()
        self.path = path
    def run(self):
        os.startfile('"'+self.path+'"')
        
def remove_tag(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    if data.has_key('ufs_url') and data.has_key('tag'):
        print data['ufs_url']
        objlist = UfsObj.objects.filter(ufs_url=data['ufs_url'])
        if 0 != objlist.count():
            tags = objlist[0].tags
            tagnames = []
            for tag in tags:
                if tag.name != data['tag']:
                    tagnames.append(tag.name)
            objlist[0].tags = ','.join(tagnames)
            print tagnames
            return HttpResponse('{"result": "remove tag done"}', mimetype="application/json")  
    return HttpResponse('{"result": "not enough params"}', mimetype="application/json")  


def get_tags(request):
    taglist = Tag.objects.usage_for_model(UfsObj)
    tagnamelist = []
    for i in taglist:
        tagnamelist.append(i.name)
    return HttpResponse(json.dumps(tagnamelist), mimetype="application/json")  


    
def start(request):
    fullpath = request.META['QUERY_STRING']
    print fullpath
    try:
        ext = os.path.splitext(fullpath)[1]
    except:
        ext = ''
    if True:#try:
        if False:#(ext in ['.bat', '.py']):
            gui_service = GuiService()
            gui_service.addItem({"command": "Launch", "path": path, "param":['--startserver']})
            #raise "stop here"
            #return "app"
        else:
            StarterThread(fullpath).start()
            #raise "stop there"
            #return "doc"
        response = '{"result": "ok", "path": %s}'%fullpath
    else:#except:
        response = '{"result": "failed", "path": %s}'%fullpath
    return HttpResponse(response, mimetype="application/json")      

    
def remove_thumb_for_paths(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    cnt = 0
    if data.has_key("path"):
        path = data["path"]
        res = []
        from libs.thumbapp.models import ThumbCache
        for i in ThumbCache.objects.filter(obj__full_path__contains=path):
            if cnt < 100:
                res.append(i.obj.full_path)
            else:
                break
        ThumbCache.objects.filter(obj__full_path__contains=path).delete()
        return HttpResponse(res, mimetype="application/json")      
