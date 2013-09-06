import os
import webbrowser
from iconizer import Iconizer
from libs.utils.filetools import findAppInProduct
import configuration


def stop_postgresql():
    os.system(findAppInProduct("postgresql_stop"))


def open_main():
    webbrowser.open("http://127.0.0.1:" + str(configuration.g_config_dict["ufs_web_server_port"]) +
                    "/objsys/manager/", new=1)

def main():
    try:
        i = Iconizer()
        i.add_close_listener(stop_postgresql)
        i.gui_launch_manger.taskbar_icon_app["Open Main Page"] = open_main
        i.execute({"ext_svr": [findAppInProduct("new_ext_svr")]})

    except (KeyboardInterrupt, SystemExit):
        raise
    #print "stopping database"


if __name__ == '__main__':
    main()
    #os.system(findAppInProduct("postgresql_stop"))