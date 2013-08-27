# -*- coding: utf8 -*-

import libsys
from libs.utils.obj_tools import get_ufs_obj_from_full_path
from libs.services.svc_base.msg_service import MsgQ
from libs.services.svc_base.msg import Msg
from libs.logsys.logSys import cl
from libs.services.svc_base.simple_service_v2 import SimpleService, SimpleServiceWorker
#from libs.services.svc_base.managed_service import ManagedService, WorkerBase
from libs.services.svc_base.gui_service import GuiService
#import urllib
from django.conf import settings
from configuration import g_config_dict
#import time
from libs.utils.string_tools import SpecialEncoder
#from ui_framework.objsys.local_obj_tools import get_ufs_obj_from_full_path

'''
class NoInputWorker(WorkerBase):
    def get_input_msg_queue_name(self):
        return
'''


class DropService(SimpleServiceWorker):
    """
    没有Service结尾的作为worker thread
    """
    def on_register_ok(self):
        """
        Called after registration is OK
        """
        super(DropService, self).on_register_ok()
        self.gui_service = GuiService()
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.gui_service.put({"command": "DropWnd", "target": self.get_input_msg_queue_name(),
                              "tip": self.param_dict.get("tip", None)})

    def process(self, msg):
        #Encode as utf8 as Django's settings.encoding is using default value: utf-8
        #See https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.encoding
        #pyqt webkit browser will quote the url passed to it? Seems yes.
        e = SpecialEncoder()
        cl(msg)
        for i in msg["urls"]:
            cl(i)
            full_path = i.replace("file:///","")
            obj = get_ufs_obj_from_full_path(full_path)
            if "tags" in self.param_dict:
                obj.tags = self.param_dict["tags"]
            msg = Msg()
            msg.add_path(obj.full_path)
            msg.add_session_id(self.param_dict.get("session_id", 0))
            msg_q = MsgQ(self.get_output_msg_queue_name())
            msg_q.send(msg)
        return True

    def on_stop(self):
        self.gui_service = GuiService()
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.gui_service.put({"command": "DestroyDropWnd",
                              "target": self.get_input_msg_queue_name()})
        return True

if __name__ == "__main__":
    s = SimpleService({
        "output": "Output msg queue for output the dropped file",
        "tags": 'default tags applied to the dropped items, use colon to separate such as tag1, tag2',
        "tip": "Tip for dropping window",
    }, worker_thread_class=DropService)
    s.run()