# Create your views here.
import json
import os
import threading
from django.http import HttpResponse
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from obj_tagging import *
from objsys.obj_operator import ObjOperator, ObjListOperator, handle_operation_request
from ufs_utils.django_utils import retrieve_param
from objsys.models import UfsObj
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect


log = logging.getLogger(__name__)

@login_required
def manager(request):
    data = retrieve_param(request)
    c = {"user": request.user, "tree": {"name": "left_tree", "url": "/collection_management/jstree/?node="}}
    c.update(csrf(request))
    return render_to_response('objsys/manager.html', c)


def query(request):
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
    data = retrieve_param(request)
    full_path = data["full_path"]
    log.debug(full_path)
    try:
        ext = os.path.splitext(full_path)[1]
    except:
        ext = ''
    if True:  #try:
        if ext in ['.bat', '.py']:
            from services.sap.launcher_sap import Launcher

            Launcher().start_app_with_exact_full_path_and_param_list_no_wait(full_path)
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
    if "path" in data:
        path = data["path"]
        res = []
        from thumbapp.models import ThumbCache

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


def listing(request):
    objects = UfsObj.objects.all()
    return render_to_response('objsys/listing.html', {"objects": objects, "request": request},
                              context_instance=RequestContext(request))


@login_required
def listing_with_description(request):
    objects = UfsObj.objects.filter(user=request.user, valid=True).order_by('-timestamp')
    return render_to_response('objsys/listing_with_description_in_bootstrap.html',
                              {"objects": objects, "request": request, "title": "My bookmarks",
                               "email": "richardwangwang@gmail.com", "author": "Richard"},
                              context_instance=RequestContext(request))


@login_required
def do_operation(request):
    data = retrieve_param(request)
    if ("cmd" in data) and ("pk" in data):
        operator = ObjOperator(int(data["pk"]))
        getattr(operator, data["cmd"])()
    return HttpResponseRedirect("/objsys/homepage/")


@login_required
def do_json_operation(request):
    return handle_operation_request(request)