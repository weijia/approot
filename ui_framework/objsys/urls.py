#from django.conf.urls import patterns, include, url
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
    url(r'^query/$', 'ui_framework.objsys.views.query'),
    url(r'^remove_tag/$', 'ui_framework.objsys.views.remove_tag'),
    url(r'^add_tag/$', 'ui_framework.objsys.views.add_tag'),
    url(r'^get_tags/$', 'ui_framework.objsys.views.get_tags'),
    url(r'^remove_thumb_for_paths/$', 'ui_framework.objsys.views.remove_thumb_for_paths'),
    url(r'^taglist/$', ListView.as_view(
            queryset=Tag.objects.all(),
            context_object_name='tagged_items',
            template_name='objsys/pane.html')),
    (r'^api/ufsobj/', include(ufsobj_resource.urls)),      
    #(r'^api/tag/', include(tag_resource.urls)),      
    url(r'^$', 'desktop.filemanager.views.index'),
    url(r'^.+$', 'desktop.filemanager.views.handler'),
)