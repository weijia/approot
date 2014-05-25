import logging
import sys
import thread
import time
import zipfile
from ufs_django_conf import *

from ufs_utils.short_decorator.ignore_exception import ignore_exc
from ufs_utils.web.direct_opener import open_url
from iconizer.iconizer_main import Iconizer
from app_framework.folders import get_or_create_app_data_folder
from libtool.filetools import find_callable_in_app_framework
from platform_related.executor import execute_app_from_name_and_wait_for_complete

from services.svc_base.postgres_app_starter import PostgresApp
#The following will set environment string for start web server.
import configuration
from extra_settings import init_settings
from services.pyro_service.name_server_starter import NameServerStarter
from webmanager.cmd_utils import exec_django_cmd


def sync_migrate_db():
    init_settings.init_settings()
    exec_django_cmd("syncdb,--noinput")
    #exec_django_cmd("migrate,--delete-ghost-migrations")


@ignore_exc
def trigger_create_admin():
    time.sleep(10)
    create_admin_base_url = 'http://localhost:%d/webmanager/create_admin_user'
    full_web_url = create_admin_base_url % configuration.g_config_dict["ufs_web_server_port"]
    open_url(full_web_url)


def start_app_in_iconizer(iconizer_instance, app_name):
    iconizer_instance.execute({app_name: [find_callable_in_app_framework(app_name)]})


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    PostgresApp()
    NameServerStarter()

    sync_migrate_db()
    thread.start_new_thread(trigger_create_admin, ())

    log_folder = get_or_create_app_data_folder("logs")
    i = Iconizer(log_dir=log_folder, python_executable=sys.executable)
    i.register()
    for app_name in ["distributor", "pull_service", "simple_tagging", "tag_enum_app",
                     "timer_service_app", "url_opener", "obj_importer"]:
        start_app_in_iconizer(i, app_name)

    #i.execute({"tag_distributor": [find_callable_in_app_framework("tag_distributor")]})
    #i.execute({"startBeanstalkd": [find_callable_in_app_framework("startBeanstalkd")]})
    #i.execute({"msg_based_service_mgr": [find_callable_in_app_framework("msg_based_service_mgr")]})

    thumb_port = configuration.g_config_dict.get("thumb_server_port", 8114)
    i.execute({"thumb_server": [find_callable_in_app_framework("cherrypy_server"), str(thumb_port)]})
    #execute_app_from_name_and_wait_for_complete("syncdb")
    execute_app_from_name_and_wait_for_complete("cherrypy_server")
    print "-----------------------------exiting cherrypy server"