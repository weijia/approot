import json
import threading
import uuid
from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import django.utils.timezone as timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from tagging.models import Tag
from utils.django_utils import retrieve_param
from utils.string_tools import SpecialEncoder
import utils.obj_tools as obj_tools
from objsys.models import UfsObj
from objsys.models import Description
from objsys.view_utils import get_ufs_obj_from_ufs_url


def append_tags_and_description_to_url(user, url, tags, description):
    #Tag object
    if obj_tools.is_web_url(url):
        full_path = None
        obj_qs = UfsObj.objects.filter(ufs_url=url, user=user, valid=True)
        ufs_url = url
    else:
        full_path = obj_tools.get_full_path_for_local_os(url)
        obj_qs = UfsObj.objects.filter(full_path=full_path)
        ufs_url = obj_tools.getUfsUrlForPath(full_path)

    if 0 == obj_qs.count():
        obj = UfsObj(ufs_url=ufs_url, uuid=unicode(uuid.uuid4()), timestamp=timezone.now(),
                     user=user, full_path=full_path)
        obj.save()
        obj_qs = [obj]
    description_obj, created = Description.objects.get_or_create(content=description)
    for obj in obj_qs:
        #obj.tags = tags
        Tag.objects.update_tags(obj, tags, tag_app='user:' + user.username)
        obj.descriptions.add(description_obj)
        obj.save()


class RequestWithAuth(object):
    def __init__(self, request):
        self.request = request
        self.data = retrieve_param(self.request)
        self.error_json = ''

    def is_authenticated(self):
        if ('username' in self.data) and ('password' in self.data):
            username = self.data['username']
            password = self.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    print 'login OK'
                    return True
                else:
                    # Return a 'disabled account' error message
                    print 'disabled account'
                    self.error_json = '{"error": "disabled account"}'
            else:
                # Return an 'invalid login' error message.
                print 'invalid login'
                self.error_json = '{"error": "invalid login", "username": "%s", "password": "%s"}' % (
                    username, password)
                return False
        self.error_json = '{"error": "no username and password"}'
        return False

    def get_error_json(self):
        return self.error_json


@csrf_exempt
def handle_append_tags_request(request):
    req_with_auth = RequestWithAuth(request)
    if not req_with_auth.is_authenticated():
        return HttpResponse(req_with_auth.get_error_json(), mimetype="application/json")

    tags = req_with_auth.data.get("tags", None)
    description = req_with_auth.data.get("description", None)
    addedCnt = 0
    for query_param_list in req_with_auth.data.lists():
        if query_param_list[0] == "selected_url":
            for url in query_param_list[1]:
                append_tags_and_description_to_url(request.user, url, tags, description)
                addedCnt += 1
    return HttpResponse('{"result": "OK", "added": %d}' % addedCnt, mimetype="application/json")


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
                    append_tags_and_description_to_url(request.user, url, tags, "manually added item")

    class UrlTagPair:
        def __init__(self, url, tags):
            self.url = url
            self.tags = tags

    request.session["saved_urls"] = urls
    urls_with_tags = []
    for url in urls:
        tags = []
        full_path = obj_tools.get_full_path_for_local_os(url)
        obj_qs = UfsObj.objects.filter(full_path=full_path)
        print obj_qs.count()
        if 0 != obj_qs.count():
            print 'object exists'
            for obj in obj_qs:
                print obj.tags
                tags.extend(obj.tags)
        urls_with_tags.append(UrlTagPair(url, tags))

    c = {"urls": urls, "user": request.user, "close_flag": close_flag, "urls_with_tags": urls_with_tags,
         "new_url_input": False}
    if 0 == len(urls_with_tags):
        c["new_url_input"] = True
    c.update(csrf(request))
    return render_to_response('objsys/tagging.html', c, context_instance=RequestContext(request))


def remove_tag(request):
    data = retrieve_param(request)
    if ('ufs_url' in data) and ('tag' in data):
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
    if ('ufs_url' in data) and ('tag' in data):
        obj = get_ufs_obj_from_ufs_url(data['ufs_url'])
        Tag.objects.add_tag(obj, data["tag"], tag_app='user:' + request.user.username)
        return HttpResponse('{"result": "added tag: %s to %s done"}' % (data["tag"], data["ufs_url"]),
                            mimetype="application/json")
    return HttpResponse('{"result": "not enough params"}', mimetype="application/json")



