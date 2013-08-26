# Create your views here.
import os
import threading

from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, render
from django.template import RequestContext

from libs.utils.django_utils import retrieve_param
from objsys.models import UfsObj
from tagging.models import Tag, TaggedItem
from obj_tagging import *


def manager(request):
    data = retrieve_param(request)
    c = {"user": request.user, "tree": {"name": "left_tree", "url": "/collection_management/jstree/?node="}}
    c.update(csrf(request))
    return render_to_response('objsys/manager.html', c)


def query(request):
    data = retrieve_param(request)
    c = {"user": request.user}
    c.update(csrf(request))
    return render_to_response('objsys/query.html', c)


class StarterThread(threading.Thread):
    def __init__(self, path):
        super(StarterThread, self).__init__()
        self.path = path

    def run(self):
        os.startfile('"' + self.path + '"')


def start(request):
    full_path = request.META['QUERY_STRING']
    print full_path
    try:
        ext = os.path.splitext(full_path)[1]
    except:
        ext = ''
    if True:  #try:
        if False:  #(ext in ['.bat', '.py']):
            from libs.services.svc_base.launcher import Launcher

            Launcher().start_app_with_exact_full_path_and_param_list_no_wait(full_path, ['--startserver'])
            #raise "stop here"
            #return "app"
        else:
            StarterThread(full_path).start()
            #raise "stop there"
            #return "doc"
        response = '{"result": "ok", "path": %s}' % full_path
    else:#except:
        response = '{"result": "failed", "path": %s}' % full_path
    return HttpResponse(response, mimetype="application/json")


def remove_thumb_for_paths(request):
    data = retrieve_param(request)
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
            cnt += 1
        ThumbCache.objects.filter(obj__full_path__contains=path).delete()
        return HttpResponse(res, mimetype="application/json")


def rm_objs_for_path(request):
    data = retrieve_param(request)
    cnt = 0
    if "ufs_url" in data:
        res = []
        prefix = data["ufs_url"]
        if prefix[-1] != "/":
            prefix += "/"
        for i in UfsObj.objects.filter(ufs_url__startswith=prefix):
            if cnt < 100:
                res.append(i.full_path)
            else:
                break
            cnt += 1
            #Remove tags first?
        #TaggedItem.objects.filter(object__ufs_url__startswith=data["ufs_url"]).delete()
        UfsObj.objects.filter(ufs_url__startswith=prefix).delete()
        return HttpResponse(res, mimetype="application/json")


def rm_obj_from_db(request):
    data = retrieve_param(request)
    if "ufs_url" in data:
        for obj in UfsObj.objects.filter(ufs_url=data["ufs_url"]):
            obj.tags = ""
            obj.delete()
        return HttpResponse('{"result": "removed: %s"}' % (data["ufs_url"]), mimetype="application/json")
    return HttpResponse('{"result": "not enough params"}', mimetype="application/json")


def listing(request):
    objects = UfsObj.objects.all()
    return render_to_response('objsys/listing.html', {"objects": objects, "request": request},
                              context_instance=RequestContext(request))

def listing_with_description(request):
    objects = UfsObj.objects.filter(user=request.user)
    return render_to_response('objsys/listing_with_description.html', {"objects": objects, "request": request},
                              context_instance=RequestContext(request))


def create_admin_user(request):
    from django.contrib.auth import models as auth_models

    auth_models.User.objects.create_superuser('admin', 'r@j.cn', 'admin')
    return HttpResponse("Done")


def homepage(request):
    context = {}
    context['ufs_objs'] = UfsObj.objects.filter(user=request.user)
    return render(request, 'objsys/index.html', context)