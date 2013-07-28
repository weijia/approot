#from django.conf.urls import patterns, include, url
#import libsys
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from models import UfsObj
import os
from django.views.generic import DetailView, ListView
from tagging.models import Tag
from api import UfsObjResource


ufsobj_resource = UfsObjResource()
#tag_resource = TagResource()

urlpatterns = patterns('',
    url(r'^tagging/$', 'ui_framework.objsys.views.tagging'),
    url(r'^manager/$', 'ui_framework.objsys.views.manager'),
    url(r'^listing/$', 'ui_framework.objsys.views.listing'),
    url(r'^qrcode/$', 'thumbapp.views.gen_qr_code'),
    url(r'^image/$', 'thumbapp.views.image'),
    url(r'^apply_tags_to/$', 'ui_framework.objsys.views.apply_tags_to'),
    url(r'^remove_tags_from/$', 'ui_framework.objsys.views.remove_tags_from'),
    url(r'^query/$', 'ui_framework.objsys.views.query'),
    url(r'^remove_tag/$', 'ui_framework.objsys.views.remove_tag'),
    url(r'^add_tag/$', 'ui_framework.objsys.views.add_tag'),
    url(r'^get_tags/$', 'ui_framework.objsys.views.get_tags'),
    url(r'^remove_thumb_for_paths/$', 'ui_framework.objsys.views.remove_thumb_for_paths'),
    url(r'^rm_objs_for_path/$', 'ui_framework.objsys.views.rm_objs_for_path'),
    url(r'^rm_obj_from_db/$', 'ui_framework.objsys.views.rm_obj_from_db'),
    url(r'^taglist/$', ListView.as_view(
            queryset=Tag.objects.all(),
            context_object_name='tagged_items',
            template_name='objsys/pane.html')),
    (r'^api/ufsobj/', include(ufsobj_resource.urls)),      
    #(r'^api/tag/', include(tag_resource.urls)),      
    #url(r'^$', 'desktop.filemanager.views.index'),
    #url(r'^.+$', 'desktop.filemanager.views.handler'),
)