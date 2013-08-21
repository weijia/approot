from django.conf.urls import patterns, include, url
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

#Permission query not found related error, use the following fix
admin.autodiscover()
#According to http://hqman.iteye.com/blog/1217856
import django.contrib.sites.admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rootapp.views.home', name='home'),
    # url(r'^rootapp/', include('rootapp.foo.urls')),
    
    (r'^accounts/', include('allauth.urls')),
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html' }),
    url(r'^accounts/profile/$', 'django.views.generic.simple.direct_to_template', {'template': 'profile.html' }),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^filemanager/', include('desktop.filemanager.urls')),                       
    url(r'^ui_framework/', include('ui_framework.urls')),                       
    #url(r'^$', redirect_to, {'url': '/filemanager/'}),
    url(r'^objsys/', include('ui_framework.objsys.urls')),
    url(r'^collection_management/', include('ui_framework.collection_management.urls')),
    url(r'^tags/', include('tags.urls')),
    url(r'^connection/', include('ui_framework.connection.urls')),
    url(r'^normal_admin/', include('ui_framework.normal_admin.urls')),
    url(r'^mapping_driver/', include('win_smb.urls')),
    url(r'^object_filter/', include('object_filter.urls')),
    url(r'^thumb/', include('thumbapp.urls')),
    url(r'', include('social_auth.urls')),
)

##############################
# The following is added for create setup for Django
##############################
from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



#Added for all other static js
'''
urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': os.path.join(settings.PROJECT_PATH, "static/"),
    }),
)
'''