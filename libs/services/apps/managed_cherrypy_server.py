import threading
import libsys
from libs.services.svc_base.simple_service_v2 import SimpleService
import cherrypy
from libs.services.svc_base.singleton_service_base import SingletonServiceBase
from cherrypy_server import Server


class CherryPyServerThread(threading.Thread):
    def __init__(self, port):
        super(CherryPyServerThread, self).__init__()
        self.port = port

    def run(self):
        Server(self.port).run()


class CherryPyServerService(SingletonServiceBase):
    def on_register_ok(self):
        #Start cherry py server
        port = int(self.param_dict["port"])
        self.server = CherryPyServerThread(port)
        self.server.start()

    def on_stop(self):
        cherrypy.engine.exit()


if __name__ == "__main__":
    s = SimpleService(
        {
            "port": "Server port"
        },
        CherryPyServerService)
    s.run()