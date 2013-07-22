#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'^connection/$', 'ui_framework.connection.views.create_diagram_obj'),
    url(r'^diagram_list/$', 'ui_framework.connection.views.get_diagrams'),
    url(r'^save_diagram/$', 'ui_framework.connection.save_diagram_view.handle_save_diagram'),
    url(r'^start_diagram/$', 'ui_framework.connection.views.handle_start_diagram_req'),
    url(r'^stop_diagram/$', 'ui_framework.connection.views.handle_stop_diagram_req'),
    url(r'^properties/$', 'ui_framework.connection.views.item_properties'),
    url(r'app_list/$', 'ui_framework.connection.views.get_service_apps'),
    url(r'^$', 'ui_framework.connection.views.index')    
)