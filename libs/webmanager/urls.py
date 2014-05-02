from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^cmd/$', 'webmanager.views.cmd'),
    url(r'^django_version/$', 'webmanager.views.version'),
    url(r'^create_admin_user/$', 'webmanager.views.handle_create_admin_req'),
)

# The following can be used to do mail backend testing
try:
    import backends.mail_backend
    urlpatterns.extend([url(r'^test_email/$', 'backends.mail_backend.mail_backend_test')])
except ImportError:
    pass