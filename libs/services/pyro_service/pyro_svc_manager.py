import traceback
import Pyro4
from iconizer.pyro_launcher import Launcher
from services.svc_base.svc_manager_base import ServiceManagerBase


class PyroServiceManager(ServiceManagerBase):
    def start_service(self, service_name):
        #super(PyroServiceManager, self).start_service(service_name)
        Launcher.start_app_with_same_filename_with_param_dict_no_wait(service_name, [])

    def stop_service(self, service_name):
        #super(PyroServiceManager, self).stop_service(service_name)
        print "stopping: ", service_name
        uri_string = "PYRONAME:" + service_name
        service = Pyro4.Proxy(uri_string)
        # Must use a try catch block to prevent the following function call to generate exception.
        #noinspection PyBroadException
        try:
            service.pyro_shutdown()
        except:
            traceback.print_exc()
