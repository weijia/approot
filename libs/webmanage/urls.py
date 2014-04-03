#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'^cmd/$', 'webmanage.views.cmd'),
    url(r'^syncdb/$', 'webmanage.views.index'),
    url(r'^django_version/$', 'webmanage.views.version'),
    url(r'^create_admin_user/$', 'webmanage.views.create_admin'),
    #url(r'^test_email/$', 'backends.mail_backend.mail_backend_test'),
)