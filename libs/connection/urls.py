#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    #url(r'^connection/$', 'connection.views.create_diagram_obj'),
    url(r'^services_list_tastypie_format/$', 'ufs_diagram.service.list_in_tastypie_format'),
    url(r'^diagram_list/$', 'connection.views.get_diagrams'),
    url(r'^save_diagram/$', 'connection.save_diagram_view.handle_save_diagram'),
    url(r'^start_diagram/$', 'connection.views.handle_start_diagram_req'),
    url(r'^stop_diagram/$', 'connection.views.handle_stop_diagram_req'),
    url(r'^properties/$', 'connection.views.item_properties'),
    url(r'app_list/$', 'connection.views.get_service_apps'),
    url(r'^$', 'connection.views.index')
)