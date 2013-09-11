import os
import traceback
import urllib2
import webbrowser
from iconizer import Iconizer
from libs.utils.filetools import findAppInProduct
import configuration


def stop_postgresql():
    os.system(findAppInProduct("postgresql_stop"))


def stop_web_servers():
    print "stopping web servers"
    try:
        urllib2.urlopen('http://localhost:%d/stop/quit' % configuration.g_config_dict["ufs_web_server_port"] )
        urllib2.urlopen('http://localhost:%d/stop/quit' % configuration.g_config_dict["thumb_server_port"] )
    except:
        traceback.print_exc()

def open_main():
    webbrowser.open("http://127.0.0.1:" + str(configuration.g_config_dict["ufs_web_server_port"]) +
                    "/objsys/manager/", new=1)

def main():
    try:
        i = Iconizer()
        i.add_close_listener(stop_web_servers)
        i.add_final_close_listener(stop_postgresql)
        i.get_gui_launch_manager().taskbar_icon_app["Open Main Page"] = open_main
        i.execute({"new_ext_svr": [findAppInProduct("new_ext_svr")]})

    except (KeyboardInterrupt, SystemExit):
        raise
    #print "stopping database"


if __name__ == '__main__':
    main()
    #os.system(findAppInProduct("postgresql_stop"))