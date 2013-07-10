#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'^root$', 'desktop.filemanager.folder_view.root'),
    url(r'^$', 'desktop.filemanager.views.index'),
    url(r'^.+$', 'desktop.filemanager.views.handler'),
)