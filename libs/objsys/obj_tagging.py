import json
import logging
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
from django.views.generic import TemplateView
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


class AddTagTemplateView(TemplateView):
    template_name = 'objsys/tagging.html'
    http_method_names = ["post", "get"]

    def __init__(self, **kwargs):
        super(AddTagTemplateView, self).__init__(**kwargs)
        self.encoding = None
        self.tags = []
        self.tagged_urls = []
        self.stored_url = []
        self.listed_urls = []

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AddTagTemplateView, self).get_context_data(**kwargs)
        data = retrieve_param(self.request)

        #Load saved submitted_url
        if "saved_urls" in self.request.session:
            self.stored_url = self.request.session["saved_urls"]

        close_flag = False
        self.retrieve_encoding(data)

        if "tags" in data:
            self.tags = data["tags"]

        decoder = SpecialEncoder()

        for query_param_list in data.lists():
            if query_param_list[0] == "url":
                all_urls = []
                for submitted_url in query_param_list[1]:
                    all_urls.append(decoder.decode(submitted_url))
                self.stored_url.extend(all_urls)
                for submitted_url in self.stored_url:
                    if not (submitted_url in self.listed_urls):
                        #print query_param_list, urls
                        self.listed_urls.append(submitted_url)
            if query_param_list[0] == 'selected_url':
                close_flag = True
                for submitted_url in query_param_list[1]:
                    self.tag_url(submitted_url)

        self.request.session["saved_urls"] = self.listed_urls

        urls_with_tags = self.get_urls_with_tags()

        c = {"user": self.request.user, "close_flag": close_flag, "urls_with_tags": urls_with_tags,
             "new_url_input": False}
        if 0 == len(urls_with_tags):
            c["new_url_input"] = True
        c.update(csrf(self.request))
        context.update(c)
        #log = logging.getLogger(__name__)
        #log.error(context)
        return context


    def retrieve_encoding(self, data):
        if "encoding" in data:
            self.encoding = data["encoding"]
        else:
            self.encoding = "utf8"

    def get_url_tags(self, url_for_ufs_obj):
        tags = []
        if obj_tools.is_web_url(url_for_ufs_obj):
            obj_qs = UfsObj.objects.filter(ufs_url=url_for_ufs_obj)
        else:
            full_path = obj_tools.get_full_path_for_local_os(url_for_ufs_obj)
            obj_qs = UfsObj.objects.filter(full_path=full_path)
            #print obj_qs.count()
        if 0 != obj_qs.count():
            #print 'object exists'
            for obj in obj_qs:
                #print obj.tags
                tags.extend(obj.tags)
        return tags

    def get_urls_with_tags(self):
        class UrlTagPair:
            def __init__(self, url, tags):
                self.url = url
                self.tags = tags
        urls_with_tags = []
        for listed_url in self.listed_urls:
            tags_for_existing_url = self.get_url_tags(listed_url)
            urls_with_tags.append(UrlTagPair(listed_url, tags_for_existing_url))
        return urls_with_tags

    def tag_url(self, url_to_tag):
        if not (url_to_tag in self.tagged_urls):
            self.tagged_urls.append(url_to_tag)
            append_tags_and_description_to_url(self.request.user, url_to_tag, self.tags, "manually added item")


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



