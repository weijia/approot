#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'^jstree/', 'ui_framework.collection_management.views.collections_jstree'),
    url(r'^$', 'ui_framework.collection_management.views.collections')
)