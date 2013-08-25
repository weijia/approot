# -*- coding: gbk -*- 
"""
This example is based on folder_expand_service
"""
import os
import time
import libsys
from libs.logsys.logSys import cl, info
from libs.services.svc_base.msg import Msg
from libs.services.svc_base.simple_service_v2 import SimpleService
from libs.services.svc_base.service_base import ThreadedService
import libs.utils.transform as transform


class ExampleSingleThreadServiceNoInputMsgQNeeded(ThreadedService):
    def run(self):
        while not self.is_quitting():
            pass


if __name__ == "__main__":
    s = SimpleService({},
                      worker_thread_class=ExampleSingleThreadServiceNoInputMsgQNeeded)
    s.run()