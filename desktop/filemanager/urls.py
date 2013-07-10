#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'^root/$', 'desktop.filemanager.folders.root'),
    url(r'^$', 'desktop.filemanager.views.index'),
    url(r'^.+$', 'desktop.filemanager.views.handler'),
)