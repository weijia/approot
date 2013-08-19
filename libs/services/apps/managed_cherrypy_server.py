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
    def is_thumb_server(self):
        is_thumb_server_param = self.param_dict.get("is_thumb_server", None)
        if (is_thumb_server_param is None) or ("false" in is_thumb_server_param.lower()):
            return False
        else:
            return True
    def on_register_ok(self):
        import configuration
        if self.is_thumb_server():
            print 'Starting thumb server'
            port = int(configuration.g_config_dict["thumb_server_port"])
        else:
            print "Starting web server"
            port = int(configuration.g_config_dict["ufs_web_server_port"])
        self.server = CherryPyServerThread(port)
        self.server.start()

    def on_stop(self):
        cherrypy.engine.exit()

    def get_task_signature(self):
        if self.is_thumb_server():
            return super(SingletonServiceBase, self).get_task_signature()+"thumb_server"
        return super(SingletonServiceBase, self).get_task_signature()

if __name__ == "__main__":
    s = SimpleService(
        {
            #"port": "Server port"
            "is_thumb_server": "If it is a thumbnail server"
        },
        CherryPyServerService)
    s.run()