# -*- coding: utf8 -*-
import libsys
from libs.logsys.logSys import cl
from libs.services.svc_base.simple_service_v2 import SimpleService
from libs.services.svc_base.managed_service import ManagedService, WorkerBase
from libs.services.svc_base.gui_service import GuiService
#import urllib
from django.conf import settings
from configuration import g_config_dict
#import time
from libs.utils.string_tools import SpecialEncoder


class DropService(WorkerBase):
    """
    没有Service结尾的作为worker thread
    """
    def worker_init(self):
        cl("--------------------------")
        self.gui_service = GuiService()
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.gui_service.put({"command": "DropWnd", "target": self.get_input_msg_queue_name(),
                              "tip": self.param_dict["tip"]})

    def process(self, msg):
        #Encode as utf8 as Django's settings.encoding is using default value: utf-8
        #See https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.encoding
        #pyqt webkit browser will quote the url passed to it? Seems yes.
        e = SpecialEncoder()
        cl(msg)
        for i in msg["urls"]:
            print i
        return True

if __name__ == "__main__":
    s = SimpleService({
        "output": "Output msg queue for output the dropped file",
        "tip": "Tip for dropping window"
    }, worker_thread_class=DropService)
    s.run()