__author__ = 'Richard'
import Pyro4
from services.sap.launcher_sap import Launcher


class NameServerStarter(object):
    def __init__(self):
        ###########################
        # Start postgresql
        ###########################
        Launcher.start_app_with_name_param_list_no_wait('name_server_app')

        cnt = 0
        while cnt < 40:
            try:
                ns = Pyro4.locateNS()
                print "Name Server started OK"
                break
            except Exception:
                import traceback
                traceback.print_exc()


if __name__ == "__main__":
    NameServerStarter()