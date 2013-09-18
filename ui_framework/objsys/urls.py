#from django.conf.urls import patterns, include, url
#import libsys
from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView
from tagging.models import Tag
from api import UfsObjResource


ufsobj_resource = UfsObjResource()
#tag_resource = TagResource()

urlpatterns = patterns('',
    url(r'^tagging/$', 'objsys.views.tagging'),
    url(r'^manager/$', 'objsys.views.manager'),
    url(r'^listing/$', 'objsys.views.listing'),
    url(r'^homepage/$', 'objsys.views.listing_with_description'),
    #url(r'^qrcode/$', 'thumbapp.views.gen_qr_code'),
    #url(r'^image/$', 'thumbapp.views.image'),
    url(r'^append_tags/$', 'objsys.views.handle_append_tags_request'),
    url(r'^apply_tags_to/$', 'objsys.views.apply_tags_to'),
    url(r'^remove_tags_from/$', 'objsys.views.remove_tags_from'),
    url(r'^query/$', 'objsys.views.query'),
    url(r'^operations/$', 'objsys.views.do_operations'),
    url(r'^remove_tag/$', 'objsys.views.remove_tag'),
    url(r'^add_tag/$', 'objsys.views.add_tag'),
    url(r'^get_tags/$', 'objsys.views.get_tags'),
    url(r'^remove_thumb_for_paths/$', 'objsys.views.remove_thumb_for_paths'),
    url(r'^rm_objs_for_path/$', 'objsys.views.rm_objs_for_path'),
    url(r'^rm_obj_from_db/$', 'objsys.views.rm_obj_from_db'),
    url(r'^taglist/$', ListView.as_view(
            queryset=Tag.objects.all(),
            context_object_name='tagged_items',
            template_name='objsys/pane.html')),
    (r'^api/ufsobj/', include(ufsobj_resource.urls)),      
    #(r'^api/tag/', include(tag_resource.urls)),      
    #url(r'^$', 'desktop.filemanager.views.index'),
    #url(r'^.+$', 'desktop.filemanager.views.handler'),
    url(r'^create_admin_user/$', 'objsys.views.create_admin_user'),
    #url(r'^homepage_all/$', 'objsys.views.homepage'),
)