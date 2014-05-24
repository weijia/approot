from django.conf.urls import patterns, include, url
from url_based_task_apps.obj_export_task import ObjExportTask


urlpatterns = patterns('',
    url(r'^export/(?P<user_id>\d+)/$', ObjExportTask.as_view(), name="export_data"),
)