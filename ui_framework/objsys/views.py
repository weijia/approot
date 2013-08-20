# Create your views here.
#from django.template import Context, loader
#from django.http import HttpResponse
import os
import json
import uuid
from django.contrib.auth import authenticate, login

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
import django.utils.timezone as timezone
#from libs.logsys.logSys import cl
from libs.tagging.utils import parse_tag_input
from libs.utils.django_utils import retrieve_param
from models import UfsObj
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from libs.utils.string_tools import SpecialEncoder
import libs.utils.obj_tools as objtools
from tagging.models import Tag, TaggedItem
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt

def append_tags_to_url(user, tags, url):
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
    if objtools.is_web_url(url):
        full_path = None
        obj_qs = UfsObj.objects.filter(ufs_url=url)
        ufs_url = url
    else:
        full_path = objtools.get_full_path_for_local_os(url)
        obj_qs = UfsObj.objects.filter(full_path=full_path)
        ufs_url = objtools.getUfsUrlForPath(full_path)

    if 0 == obj_qs.count():
        obj = UfsObj(ufs_url=ufs_url, uuid=unicode(uuid.uuid4()), timestamp=timezone.now(),
                     user=user, full_path=full_path)
        obj.save()
        obj_qs = [obj]

    for obj in obj_qs:
        #obj.tags = tags
        Tag.objects.update_tags(obj, tags, tag_app='user:' + user.username)


@csrf_exempt
def handle_append_tags_request(request):
    data = retrieve_param(request)
    if not request.user.is_authenticated():
        # Do something for authenticated users.
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

            else:
                # Return a 'disabled account' error message
                print 'disabled account'
                return HttpResponse('{"error": "disabled account"}', mimetype="application/json")
        else:
            # Return an 'invalid login' error message.
            print 'invalid login'
            return HttpResponse('{"error": "invalid login", "username": "%s", "password": "%s"}' % (username, password),
                                mimetype="application/json")

    if "tags" in data:
        tags = data["tags"]
        for query_param_list in data.lists():
            if query_param_list[0] == "selected_url":
                for url in query_param_list[1]:
                    append_tags_to_url(request.user, tags, url)
    return HttpResponse('{"result": "OK"}', mimetype="application/json")

@login_required
def tagging(request):
    data = retrieve_param(request)

    #Load saved url
    if "saved_urls" in request.session:
        stored_urls = request.session["saved_urls"]
    else:
        stored_urls = []
    selected_url = []
    urls = []
    close_flag = False
    if "encoding" in data:
        encoding = data["encoding"]
    else:
        encoding = "utf8"

    if "tags" in data:
        tags = data["tags"]
    else:
        tags = []
        #print tags
    decoder = SpecialEncoder()

    for query_param_list in data.lists():
        if query_param_list[0] == "url":
            all_urls = []
            for url in query_param_list[1]:
                all_urls.append(decoder.decode(url))
            stored_urls.extend(all_urls)
            for url in stored_urls:
                if not (url in urls):
                    #print query_param_list, urls
                    urls.append(url)
        if query_param_list[0] == 'selected_url':
            close_flag = True
            for url in query_param_list[1]:
                if not (url in selected_url):
                    selected_url.append(url)
                    append_tags_to_url(request.user, tags, url)

    class UrlTagPair:
        def __init__(self, url, tags):
            self.url = url
            self.tags = tags

    request.session["saved_urls"] = urls
    urls_with_tags = []
    for url in urls:
        tags = []
        full_path = objtools.get_full_path_for_local_os(url)
        obj_qs = UfsObj.objects.filter(full_path=full_path)
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
    data = retrieve_param(request)
    c = {"user": request.user, "tree": {"name": "left_tree", "url": "/collection_management/jstree/?node="}}
    c.update(csrf(request))
    return render_to_response('objsys/manager.html', c)


def query(request):
    data = retrieve_param(request)
    c = {"user": request.user}
    c.update(csrf(request))
    return render_to_response('objsys/query.html', c)


import threading


class StarterThread(threading.Thread):
    def __init__(self, path):
        super(StarterThread, self).__init__()
        self.path = path

    def run(self):
        os.startfile('"' + self.path + '"')


def remove_tag(request):
    data = retrieve_param(request)
    if data.has_key('ufs_url') and data.has_key('tag'):
        #print data['ufs_url']
        obj_list = UfsObj.objects.filter(ufs_url=data['ufs_url'])
        if 0 != obj_list.count():
            tags = obj_list[0].tags
            tag_name = []
            for tag in tags:
                if tag.name != data['tag']:
                    tag_name.append(tag.name)
            obj_list[0].tags = ','.join(tag_name)
            print tag_name
            return HttpResponse('{"result": "remove tag done"}', mimetype="application/json")
    return HttpResponse('{"result": "not enough params"}', mimetype="application/json")


def get_tags(request):
    tag_list = Tag.objects.usage_for_model(UfsObj)
    tag_name_list = []
    for i in tag_list:
        tag_name_list.append(i.name)
    return HttpResponse(json.dumps(tag_name_list), mimetype="application/json")


def add_tag(request):
    data = retrieve_param(request)
    if data.has_key('ufs_url') and data.has_key('tag'):
        obj = get_ufs_obj_from_ufs_url(data['ufs_url'])
        Tag.objects.add_tag(obj, data["tag"], tag_app='user:' + request.user.username)
        return HttpResponse('{"result": "added tag: %s to %s done"}' % (data["tag"], data["ufs_url"]),
                            mimetype="application/json")
    return HttpResponse('{"result": "not enough params"}', mimetype="application/json")


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
    return render_to_response('objsys/listing.html', {"objects": objects},
                              context_instance=RequestContext(request))


class UfsFilter(object):
    def set_data(self, data):
        self.data = data

    def set_tag_app(self, tag_app):
        self.tag_app = tag_app

    def get_obj_filters(self):
        #print "Filtering"
        q = UfsObj.objects.all()
        if "existing_tags" in self.data:
            existing_tags = self.data["existing_tags"]
            if existing_tags:
                #cl(existing_tags)
                tags = existing_tags.split(",")
                q = TaggedItem.objects.get_by_model(UfsObj, Tag.objects.filter(name__in=tags))
        if "url_contains" in self.data:
            url_contains = self.data["url_contains"]
            if url_contains:
                #cl(url_prefix)
                q = q.filter(ufs_url__contains=url_contains)
        if "full_path_contains" in self.data:
            full_path_contains = self.data["full_path_contains"]
            if full_path_contains:
                #cl(full_path_prefix)
                q = q.filter(full_path__contains=full_path_contains)
        return q


class ApplyTagsThread(UfsFilter, threading.Thread):

    def run(self):
        if not ("tags" in self.data):
            return

        for obj in self.get_obj_filters():
            #print obj
            #obj.tags = self.data["tags"]
            Tag.objects.add_tag(obj, self.data["tags"], tag_app=self.tag_app)


class RemoveTagsThread(UfsFilter, threading.Thread):
    def run(self):
        if not ("tags" in self.data):
            return

        for obj in self.get_obj_filters():
            #print obj
            #obj.tags = self.data["tags"]
            removing_tag_list = parse_tag_input(self.data["tags"])
            final_tags = []
            for tag in obj.tags:
                if not (tag.name in removing_tag_list):
                    final_tags.append(tag.name)
            obj.tags = ",".join(final_tags)


def apply_tags_to(request):
    data = retrieve_param(request)
    t = ApplyTagsThread()
    t.set_data(data)
    t.set_tag_app('user:' + request.user.username)
    t.start()
    return HttpResponse('{"result": "Apply tags processing"}', mimetype="application/json")


def remove_tags_from(request):
    data = retrieve_param(request)
    t = RemoveTagsThread()
    t.set_data(data)
    t.set_tag_app('user:' + request.user.username)
    t.start()
    return HttpResponse('{"result": "Remove tags processing"}', mimetype="application/json")
	
	

def create_admin(request):
    #user = User.objects.create_user('richard', 'r@j.cn', 'johnpassword')
    #from django.contrib.auth.create_superuser import createsuperuser
    #createsuperuser()
    from django.contrib.auth import models as auth_models
    auth_models.User.objects.create_superuser('admin', 'r@j.cn', 'admin')
    return HttpResponse("Done")