import traceback
import Pyro4
from services.svc_base.svc_manager_base import ServiceManagerBase


class PyroServiceManager(ServiceManagerBase):
    def stop_service(self, service_name):
        print "stopping: ", service_name
        uri_string = "PYRONAME:" + service_name
        service = Pyro4.Proxy(uri_string)
        # Must use a try catch block to prevent the following function call to generate exception.
        try:
            service.pyro_shutdown()
        except:
            traceback.print_exc()
