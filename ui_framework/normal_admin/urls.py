from django.conf.urls import patterns, include, url
from django.contrib import admin
from ui_framework.normal_admin.admin import user_admin_site
 
#Permission query not found related error, use the following fix
#admin.autodiscover()
#According to http://hqman.iteye.com/blog/1217856
import django.contrib.sites.admin
 
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(user_admin_site.urls)),
    #url(r'^', include('myapp.urls')),
)