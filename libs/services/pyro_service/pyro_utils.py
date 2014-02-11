import Pyro4
import traceback


def shutdown_all():
    ns = Pyro4.locateNS()
    service_dict = ns.list()
    basic_services = ["Pyro.NameServer", "ufs_launcher"]

    for service_name in service_dict:
        if service_name in basic_services:
            continue
        print "stopping: ", service_name
        uri_string = "PYRONAME:"+service_name
        service = Pyro4.Proxy(uri_string)
        # Must use a try catch block to prevent the following function call to generate exception.
        try:
            service.shutdown()
        except:
            traceback.print_exc()
