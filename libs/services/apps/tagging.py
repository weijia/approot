import libsys
from libs.services.svc_base.service_base import MsgProcessor
from libs.services.svc_base.gui_service import GuiService
import urllib
from django.conf import settings
from configuration import g_config_dict
import time
from libs.utils.string_tools import SpecialEncoder


class TaggingService(MsgProcessor):
    def __init__(self):
        super(TaggingService, self).__init__({"input_msg_q_name": "system_tagging_service_input_msg_q"})
        self.gui_service = GuiService()
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.gui_service.put({"command": "DropWnd", "target": self.get_input_msg_queue_name()})

    def process(self, msg):
        #Encode as utf8 as django's settings.encoding is using default value: utf-8
        #See https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.encoding
        #pyqt webkit browser will quote the url passed to it? Seems yes.
        links = ""
        e = SpecialEncoder()
        for i in msg["urls"]:
            links += "url=" + e.encode(unicode(i)).encode(settings.DEFAULT_CHARSET) + "&"
        self.gui_service.put({"command": "Browser", "url": "http://127.0.0.1:" + str(
            g_config_dict["ufs_web_server_port"]) + "/objsys/tagging/?" +
                                                           links + "encoding=" + settings.DEFAULT_CHARSET,
                              "handle": "tagging"})
        #To avoid adding several files at the same time
        #time.sleep(2)
        return True


if __name__ == "__main__":
    s = TaggingService()
    s.startServer()