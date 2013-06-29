#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'^$', 'tags.views.tag_list'),
    url(r'^tagged/.*', 'tags.views.list_tagged'),
    url(r'^pane/', 'tags.views.pane'),
    
)