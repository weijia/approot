import os
import traceback
import urllib2
import uuid
import webbrowser
from libs.utils.syspath import include_file_sibling_folder
include_file_sibling_folder(__file__, "libs")
from iconizer import Iconizer
from libs.app_framework.folders import get_or_create_app_data_folder
from libs.msg import BeanstalkMsgService
from libs.utils.filetools import find_callable_in_app_framework
import configuration
from services.pyro_service.pyro_utils import shutdown_all


def stop_postgresql():
    os.system(find_callable_in_app_framework("postgresql_stop"))


def ignore_exc(func):
    def wrap_with_exc():
        try:
            func()
        except:
            #traceback.print_exc()
            pass
    return wrap_with_exc


@ignore_exc
def stop_main_server():
    urllib2.urlopen('http://localhost:%d/stop/quit' % configuration.g_config_dict["ufs_web_server_port"])


@ignore_exc
def stop_thumb_server():
    urllib2.urlopen('http://localhost:%d/stop/quit' % configuration.g_config_dict["thumb_server_port"])


def stop_services_and_web_servers():
    print "stopping services"
    shutdown_all()
    print "stopping web servers"
    stop_main_server()
    stop_thumb_server()


def open_main():
    webbrowser.open("http://127.0.0.1:" + str(configuration.g_config_dict["ufs_web_server_port"]) +
                    "/objsys/manager/", new=1)


def main():
    os.environ["UFS_CONSOLE_MGR_SESSION_ID"] = str(uuid.uuid4())
    try:
        log_folder = get_or_create_app_data_folder("logs")
        i = Iconizer(log_folder, BeanstalkMsgService())
        #i.start_name_server()
        i.add_close_listener(stop_services_and_web_servers)
        i.add_final_close_listener(stop_postgresql)
        i.get_gui_launch_manager().taskbar_icon_app["Open Main Page"] = open_main
        import configuration
        i.execute({"new_ext_svr": [find_callable_in_app_framework("new_ext_svr")]})

    except (KeyboardInterrupt, SystemExit):
        raise
        #print "stopping database"


if __name__ == '__main__':
    main()
    #os.system(findAppInProduct("postgresql_stop"))