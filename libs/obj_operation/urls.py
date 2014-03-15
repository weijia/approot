#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'service/start/$', 'obj_operation.service_op.start'),
    url(r'service/stop/$', 'obj_operation.service_op.stop'),
)