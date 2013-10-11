import os
import traceback
import urllib2
import uuid
import webbrowser
from iconizer import Iconizer
from libs.app_framework.folders import get_or_create_app_data_folder
from libs.utils.filetools import find_callable_in_app_framework
import configuration


def stop_postgresql():
    os.system(find_callable_in_app_framework("postgresql_stop"))


def stop_web_servers():
    print "stopping web servers"
    try:
        urllib2.urlopen('http://localhost:%d/stop/quit' % configuration.g_config_dict["ufs_web_server_port"])
        urllib2.urlopen('http://localhost:%d/stop/quit' % configuration.g_config_dict["thumb_server_port"])
    except:
        traceback.print_exc()


def open_main():
    webbrowser.open("http://127.0.0.1:" + str(configuration.g_config_dict["ufs_web_server_port"]) +
                    "/objsys/manager/", new=1)


def main():
    os.environ["UFS_CONSOLE_MGR_SESSION_ID"] = str(uuid.uuid4())
    try:
        log_folder = get_or_create_app_data_folder("logs")
        i = Iconizer(log_folder)
        i.add_close_listener(stop_web_servers)
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