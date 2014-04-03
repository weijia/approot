import threading
from django.http import HttpResponse
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input
from objsys.models import UfsObj
from utils.django_utils import retrieve_param


class UfsFilter(object):
    def __init__(self):
        self.data = None
        self.tag_app = None

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