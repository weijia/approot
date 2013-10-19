import libsys
from libs.services.svc_base.gui_client import GuiClient
from libs.services.svc_base.msg_service import AutoRouteMsgService
from libs.logsys.logSys import cl
from libs.services.svc_base.simple_service_v2 import SimpleService
from libs.services.svc_base.managed_service import ManagedService
#import urllib
from django.conf import settings
from configuration import g_config_dict
#import time
from libs.utils.string_tools import SpecialEncoder


class TaggingService(ManagedService):
    def __init__(self, param_dict):
        param_dict.update({"input": "system_tagging_service_input_msg_q"})
        super(TaggingService, self).__init__(param_dict)
        self.gui_client = GuiClient()
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.gui_client.register_drop_msg_receiver(self.get_input_msg_queue_name(), "tagging")
        self.auto_msg_service = AutoRouteMsgService()

    def process(self, msg):
        #Encode as utf8 as Django's settings.encoding is using default value: utf-8
        #See https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.encoding
        #pyqt webkit browser will quote the url passed to it? Seems yes.
        links = ""
        e = SpecialEncoder()
        cl(msg)
        for i in msg["urls"]:
            links += "url=" + e.encode(unicode(i)).encode(settings.DEFAULT_CHARSET) + "&"
        self.auto_msg_service.sendto('system_gui_service_input_msg_q', {"command": "Browser",
                              "url": "http://127.0.0.1:" +
                                    str(g_config_dict["ufs_web_server_port"]) +
                                    "/objsys/tagging/?" +
                                    links + "encoding=" + settings.DEFAULT_CHARSET,
                              "handle": "tagging"})
        #To avoid adding several files at the same time
        #time.sleep(2)
        return True

    def is_server_only(self):
        return True

    def on_stop(self):
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.gui_client.un_register_drop_msg_receiver(self.get_input_msg_queue_name())
        return True   # Return true to accept stop

if __name__ == "__main__":
    s = SimpleService({}, TaggingService)
    s.run()