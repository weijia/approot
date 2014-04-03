#from django.conf.urls import patterns, include, url
#import libsys
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView
from tagging.models import Tag
from api import UfsObjResource


ufsobj_resource = UfsObjResource()
#tag_resource = TagResource()

urlpatterns = patterns('',
    url(r'^remove_tags_from/$', 'objsys_local.views.remove_tags_from'),
    url(r'^remove_thumb_for_paths/$', 'objsys.obj_tagging.remove_thumb_for_paths'),
    url(r'^rm_objs_for_path/$', 'objsys.obj_tagging.rm_objs_for_path'),
    url(r'^rm_obj_from_db/$', 'objsys.obj_tagging.rm_obj_from_db'),
    url(r'^apply_tags_to/$', 'objsys.views.apply_tags_to'),
)