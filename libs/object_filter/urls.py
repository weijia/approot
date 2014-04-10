#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'object_filter.views.object_filter'),
    url(r'^table/$', 'object_filter.views.object_table'),
    url(r'^export_tags/$', 'object_filter.operations.handle_export_tags'),
)