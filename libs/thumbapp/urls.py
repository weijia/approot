from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to



urlpatterns = patterns('',
    url(r'^$', 'thumbapp.views.thumb'),
    url(r'^/cherry/$', 'thumbapp.views.thumb'),
    url(r'^qrcode/$', 'thumbapp.views.gen_qr_code'),
    url(r'^image/$', 'thumbapp.views.image'),
)