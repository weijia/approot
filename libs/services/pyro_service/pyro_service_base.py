import Pyro4


class PyRoServiceBase(object):
    def __init__(self):
        self.daemon = None

    def register(self, obj_name=None):
        if self.daemon is None:
            self.daemon = Pyro4.Daemon()
        else:
            raise "Already started"
        registered_obj = self.daemon.register(self)
        ns = Pyro4.locateNS()
        if obj_name is None:
            obj_name = self.__class__.__name__
            print "Registering service: ", obj_name
        ns.register(obj_name, registered_obj)
        self.daemon.requestLoop()

    def shutdown(self):
        self.daemon.shutdown()

