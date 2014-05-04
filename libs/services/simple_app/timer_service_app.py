import logging
import threading
import time
from ufs_django_conf import *
from msg_service.predefined_receivers import DISTRIBUTOR
from services.pyro_service.pyro_simple_app_base import PyroSimpleAppBase
from services.sap.msg_service_sap import AutoRouteMsgService


class TimerWorker(threading.Thread):
    def __init__(self, diagram_info, duration, is_recursive=False, group=None, target=None, name=None, args=(),
                 kwargs=None, verbose=None):
        super(TimerWorker, self).__init__(group, target, name, args, kwargs, verbose)
        self.diagram_info = diagram_info
        self.duration = duration
        self.is_recursive = is_recursive

    def run(self):
        while True:
            #time.sleep(10)#self.duration)
            AutoRouteMsgService().send_to(DISTRIBUTOR, {"diagram": self.diagram_info})
            if not self.is_recursive:
                break
            time.sleep(self.duration)


class TimerServiceApp(PyroSimpleAppBase):
    def __init__(self):
        super(TimerServiceApp, self).__init__()
        self.workers = []

    def handle_req(self, msg):
        worker = TimerWorker(msg["diagram"], msg["duration"], msg["is_recursive"])
        self.workers.append(worker)
        worker.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    timer_service = TimerServiceApp()
    timer_service.start_service()