#from django.conf.urls import patterns, include, url
#import libsys
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from tagging.models import Tag
from api import UfsObjResource
from objsys.obj_tagging import AddTagTemplateView
from objsys.rss import LatestEntriesFeed


ufsobj_resource = UfsObjResource()
#tag_resource = TagResource()

urlpatterns = patterns('',
    url(r'^tagging/$', login_required(AddTagTemplateView.as_view())),
    url(r'^tagging/(?P<news_item_pk>\d+)/$', login_required(AddTagTemplateView.as_view()), name="news-item"),
    url(r'^manager/$', 'objsys.views.manager'),
    url(r'^listing/$', 'objsys.views.listing'),
    url(r'^homepage/$', 'objsys.views.listing_with_description'),
    (r'^latest/feed/$', LatestEntriesFeed()),
    #url(r'^qrcode/$', 'thumbapp.views.gen_qr_code'),
    #url(r'^image/$', 'thumbapp.views.image'),
    url(r'^append_tags/$', 'objsys.views.handle_append_tags_request'),
    url(r'^query/$', 'objsys.views.query'),
    url(r'^operations/$', 'objsys.views.do_operations'),
    url(r'^remove_tag/$', 'objsys.obj_tagging.remove_tag'),
    url(r'^add_tag/$', 'objsys.obj_tagging.add_tag'),
    url(r'^get_tags/$', 'objsys.obj_tagging.get_tags'),
    url(r'^taglist/$', ListView.as_view(
            queryset=Tag.objects.all(),
            context_object_name='tagged_items',
            template_name='objsys/pane.html')),
    (r'^api/ufsobj/', include(ufsobj_resource.urls)),      
    #(r'^api/tag/', include(tag_resource.urls)),      
    #url(r'^$', 'desktop.filemanager.views.index'),
    #url(r'^.+$', 'desktop.filemanager.views.handler'),
    #url(r'^homepage_all/$', 'objsys.views.homepage'),
)