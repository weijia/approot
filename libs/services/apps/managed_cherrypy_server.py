import threading
import urllib2
import libsys
import configuration
from libs.services.svc_base.launcher_interface import Launcher
from libs.services.svc_base.msg import Msg
from libs.services.svc_base.simple_service_v2 import SimpleService
from libs.services.svc_base.singleton_service_base import SingletonServiceBase


class CherryPyServerService(SingletonServiceBase):

    def on_register_ok(self):

        l = Launcher()
        l.start_app_with_name_param_list_with_session_no_wait("cherrypy_server",
                    ["%d" % configuration.g_config_dict["thumb_server_port"],])
        l.start_app_with_name_param_list_with_session_no_wait("cherrypy_server",
                    ["%d" % configuration.g_config_dict["ufs_web_server_port"],])

    def on_stop(self):
        urllib2.urlopen('http://localhost:%d/stop/' % configuration.g_config_dict["ufs_web_server_port"] )
        urllib2.urlopen('http://localhost:%d/stop/' % configuration.g_config_dict["thumb_server_port"] )

    def is_server_only(self):
        return True

def main():
    s = SimpleService(
        {
        },
        CherryPyServerService)
    s.run()

if __name__ == "__main__":
    main()