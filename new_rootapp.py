import logging
import os
import uuid
import webbrowser
from ufs_django_conf import *
from ufs_utils.misc import ensure_dir
from ufs_utils.short_decorator.ignore_exception import ignore_exc
from ufs_utils.web.direct_opener import open_url
from iconizer import Iconizer
#The following line must has lib import prefix, don't know why
from app_framework.folders import get_or_create_app_data_folder
from libtool.filetools import find_callable_in_app_framework
from libtool.libtool import find_root_path, get_current_path, find_root
import configuration
from services.pyro_service.pyro_utils import shutdown_all


def stop_postgresql():
    os.system(find_callable_in_app_framework("postgresql_stop"))


stop_url_base = 'http://localhost:%d/stop/quit'


@ignore_exc
def stop_main_server():
    full_web_url = stop_url_base % configuration.g_config_dict["ufs_web_server_port"]
    open_url(full_web_url)


@ignore_exc
def stop_thumb_server():
    full_web_url = stop_url_base % configuration.g_config_dict["thumb_server_port"]
    open_url(full_web_url)


def stop_services_and_web_servers():
    print "stopping services"
    shutdown_all()
    print "stopping web servers"
    stop_main_server()
    stop_thumb_server()


def open_main():
    try:
        from webmanager.default_user_conf import get_default_username_and_pass
        default_admin_password, default_admin_user = get_default_username_and_pass()

        webbrowser.open("http://127.0.0.1:%s/webmanager/login_and_go_home/?username=%s&password=%s&target="
                    "/objsys/manager/" % (str(configuration.g_config_dict["ufs_web_server_port"]),
                                              default_admin_user, default_admin_password), new=1)
    except:
        webbrowser.open("http://127.0.0.1:%s/objsys/manager/" % str(configuration.g_config_dict["ufs_web_server_port"]), new=1)


def main():
    #find_root will fail when use: python new_rootapp.py.
    root_path = find_root("approot")
    log_root = os.path.join(root_path, "../data/logs")

    ensure_dir(log_root)

    os.environ["UFS_CONSOLE_MGR_SESSION_ID"] = str(uuid.uuid4())
    try:
        log_folder = get_or_create_app_data_folder("logs")
        i = Iconizer(log_folder)
        #i.start_name_server()
        i.add_close_listener(stop_services_and_web_servers)
        i.add_final_close_listener(stop_postgresql)
        i.get_gui_launch_manager().taskbar_icon_app["Open Main Page"] = open_main
        import configuration

        i.execute({"new_ext_svr": [find_callable_in_app_framework("new_ext_svr")]})
        #i.execute({"dir": ["dir"]})

    except (KeyboardInterrupt, SystemExit):
        raise
        #print "stopping database"


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
    #os.system(findAppInProduct("postgresql_stop"))