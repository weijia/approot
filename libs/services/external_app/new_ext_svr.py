import os
from iconizer.iconizer_main import Iconizer
import sys
import libsys
import django_commands_dict
from libs.app_framework.folders import get_or_create_app_data_folder
from libs.utils.filetools import find_callable_in_app_framework
from libs.platform_related.executor import execute_app_from_name_and_wait_for_complete

from libs.services.svc_base.postgres_app import PostgreSqlApp
#The following will set environment string for start web server.
#import configuration

from extra_settings import init_settings
import django.core.management as core_management
from services.svc_base.name_server_starter import NameServerStarter


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


if __name__ == "__main__":
    os.chdir(libsys.get_root_dir())
    PostgreSqlApp()
    #NameServerStarter()

    sync_migrate_db()
    log_folder = get_or_create_app_data_folder("logs")
    i = Iconizer(log_dir=log_folder, python_executable=sys.executable)
    #i.execute({"pull_service": [find_callable_in_app_framework("pull_service")]})
    #i.execute({"startBeanstalkd": [find_callable_in_app_framework("startBeanstalkd")]})
    #i.execute({"msg_based_service_mgr": [find_callable_in_app_framework("msg_based_service_mgr")]})
    #thumb_port = configuration.g_config_dict.get("thumb_server_port", 8114)
    #execute_app_from_name_and_wait_for_complete("syncdb")
    execute_app_from_name_and_wait_for_complete("cherrypy_server")
    print "-----------------------------exiting cherrypy server"
    
    
    
    