from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to



urlpatterns = patterns('',
    url(r'^$', 'thumbapp.views.thumb'),
    url(r'^/cherry/$', 'thumbapp.views.thumb'),
)