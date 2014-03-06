import Pyro4
import traceback
from Pyro4.errors import NamingError
from iconizer.iconizer_consts import ICONIZER_SERVICE_NAME


def get_name_server_without_exception():
    try:
        ns = Pyro4.locateNS()
    except NamingError:
        import traceback
        traceback.print_exc()
        ns = None
    return ns


def shutdown_all():
    ns = get_name_server_without_exception()
    if not (ns is None):
        service_dict = ns.list()
        basic_services = ["Pyro.NameServer", ICONIZER_SERVICE_NAME]

        for service_name in service_dict:
            if service_name in basic_services:
                continue
            print "stopping: ", service_name
            uri_string = "PYRONAME:"+service_name
            service = Pyro4.Proxy(uri_string)
            # Must use a try catch block to prevent the following function call to generate exception.
            try:
                service.pyro_shutdown()
            except:
                traceback.print_exc()
