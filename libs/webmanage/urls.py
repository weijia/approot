#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os


urlpatterns = patterns('',
    url(r'^cmd/$', 'webmanage.views.cmd'),
    #url(r'^syncdb/$', 'webmanage.views.index'),#Use cmd/syncdb instead of syncdb so migrate may be supported
    url(r'^django_version/$', 'webmanage.views.version'),
    url(r'^create_admin_user/$', 'webmanage.views.handle_create_admin_req'),
)


try:
    import backends.mail_backend
    urlpatterns.extend([url(r'^test_email/$', 'backends.mail_backend.mail_backend_test')])
except ImportError:
    pass