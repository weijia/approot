import inspect
import logging
import os
from threading import Thread
import Pyro4
import time


class ShutdownThread(Thread):
    def __init__(self, daemon):
        super(ShutdownThread, self).__init__()
        self.daemon = daemon

    def run(self):
        time.sleep(1)
        print "Shutdown daemon"
        self.daemon.shutdown()


log = logging.getLogger(__name__)


class PyRoServiceBase(object):
    def __init__(self):
        super(PyRoServiceBase, self).__init__()
        self.daemon = None

    @staticmethod
    def get_file_basename(file_path):
        default_name = os.path.basename(file_path).replace(".py", "").replace(".exe", "")
        return default_name

    def get_filename(self):
        frame, filename, line_number, function_name, lines, index = \
            inspect.getouterframes(inspect.currentframe())[1]
        (frame, filename, line_number, function_name, lines, index)
        return self.get_file_basename(filename)

    def register(self, obj_name=None):
        if self.daemon is None:
            self.daemon = Pyro4.Daemon()
        else:
            raise "Already started"
        registered_obj = self.daemon.register(self)
        ns = Pyro4.locateNS()
        if obj_name is None:
            frame, filename, line_number, function_name, lines, index = \
                    inspect.getouterframes(inspect.currentframe())[1]
            (frame, filename, line_number, function_name, lines, index)
            obj_name = self.get_file_basename(filename)
            print "Registering service: ", obj_name
        ns.register(obj_name, registered_obj)
        self.daemon.requestLoop()

    def shutdown(self):
        self.daemon.shutdown()
        #ShutdownThread(self.daemon).start()

    def put_msg(self, msg):
        pass