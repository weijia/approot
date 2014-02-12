import Pyro4
import psycopg2
import libsys
from libs.services.svc_base.ext_app_if import ExtAppMgrIntf
import configuration
from libs.services.svc_base.launcher_interface import Launcher
__author__ = 'Richard'


class NameServerStarter(ExtAppMgrIntf):
    def __init__(self):
        ###########################
        # Start postgresql
        ###########################
        Launcher().start_app_with_name_param_list_with_session_no_wait('name_server_app')

        cnt = 0
        while cnt < 40:
            try:
                ns = Pyro4.locateNS()
                break
            except:
                import traceback
                traceback.print_exc()
