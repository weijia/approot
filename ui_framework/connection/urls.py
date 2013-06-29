#from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
import os

urlpatterns = patterns('',
    url(r'^connection/$', 'ui_framework.connection.views.create_diagram_obj'),
    url(r'^save_diagram/$', 'ui_framework.connection.save_diagram_view.handle_save_diagram'),
    url(r'^properties/$', 'ui_framework.connection.views.item_properties'),
    url(r'^$', 'ui_framework.connection.views.index')    
)