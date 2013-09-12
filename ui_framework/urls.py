#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'^$', 'ui_framework.views.index'),
    url(r'manifest', 'ui_framework.manifest.manifest'),
    url(r'start', 'objsys.views.start'),
)