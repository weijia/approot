import logging
import os
import sys
import thread
import time
from libs.utils.short_decorator.ignore_exception import ignore_exc
from libs.utils.web.direct_opener import open_url
import libsys
from iconizer.iconizer_main import Iconizer
import django_commands_dict
from app_framework.folders import get_or_create_app_data_folder
from libtool.filetools import find_callable_in_app_framework
from platform_related.executor import execute_app_from_name_and_wait_for_complete

from services.svc_base.postgres_app_starter import PostgresApp
#The following will set environment string for start web server.
import configuration
from extra_settings import init_settings
import django.core.management as core_management
from services.pyro_service.name_server_starter import NameServerStarter


def sync_migrate_db():
    init_settings.init_settings()
    exec_django_cmd("syncdb,--noinput")
    exec_django_cmd("migrate")


def exec_django_cmd(data_params_):
    params = data_params_.split(",")
    # manage.py here is not used in execute_from_command_line, it is just used to occupy the position.
    command_line_param = ["manage.py"]
    command_line_param.extend(params)
    core_management._commands = django_commands_dict.django_commands_dict
    core_management.execute_from_command_line(command_line_param)


@ignore_exc
def trigger_create_admin():
    time.sleep(10)
    create_admin_base_url = 'http://localhost:%d/webmanage/create_admin_user'
    full_web_url = create_admin_base_url % configuration.g_config_dict["ufs_web_server_port"]
    open_url(full_web_url)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    PostgresApp()
    NameServerStarter()

    sync_migrate_db()
    thread.start_new_thread(trigger_create_admin, [])

    log_folder = get_or_create_app_data_folder("logs")
    i = Iconizer(log_dir=log_folder, python_executable=sys.executable)
    i.register()
    i.execute({"distributor": [find_callable_in_app_framework("distributor")]})
    i.execute({"pull_service": [find_callable_in_app_framework("pull_service")]})
    i.execute({"simple_tagging": [find_callable_in_app_framework("simple_tagging")]})
    i.execute({"tag_enum_app": [find_callable_in_app_framework("tag_enum_app")]})
    i.execute({"timer_service_app": [find_callable_in_app_framework("timer_service_app")]})
    #i.execute({"tag_distributor": [find_callable_in_app_framework("tag_distributor")]})
    #i.execute({"startBeanstalkd": [find_callable_in_app_framework("startBeanstalkd")]})
    #i.execute({"msg_based_service_mgr": [find_callable_in_app_framework("msg_based_service_mgr")]})
    thumb_port = configuration.g_config_dict.get("thumb_server_port", 8114)
    i.execute({"thumb_server": [find_callable_in_app_framework("cherrypy_server"), str(thumb_port)]})
    #execute_app_from_name_and_wait_for_complete("syncdb")
    execute_app_from_name_and_wait_for_complete("cherrypy_server")
    print "-----------------------------exiting cherrypy server"