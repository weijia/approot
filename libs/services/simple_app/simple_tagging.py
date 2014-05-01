import logging
import sys
import libsys
print sys.path
print sys.path
from config import get_ufs_web_server_port
from services.pyro_service.pyro_simple_app_base import PyroSimpleAppBase

from services.svc_base.gui_client import GuiClient
print sys.path
from ufs_utils.string_tools import quote_unicode

log = logging.getLogger(__name__)


class SimpleTagging(PyroSimpleAppBase):
    SERVICE_NAME = "simple_tagging"

    def __init__(self):
        super(SimpleTagging, self).__init__()
        self.gui_client = GuiClient()

    def open_drop_wnd(self):
        self.gui_client.register_drop_msg_receiver(self.SERVICE_NAME, self.SERVICE_NAME)

    def close_drop_wnd(self):
        self.gui_client.un_register_drop_msg_receiver(self.SERVICE_NAME)

    #####################
    # Override start service
    def start_service(self):
        if self.is_checking_properties():
            return
        self.open_drop_wnd()
        self.set_service_name(self.SERVICE_NAME)
        self.start_daemon_register_and_launch_loop()
        self.close_drop_wnd()

    #########################
    # Called through pyro only
    #########################
    def put_msg(self, msg):
        links = ""

        log.debug(msg)
        for i in msg["urls"]:
            links += "url=" + quote_unicode(unicode(i)) + "&"
        self.gui_client.open_browser({"command": "Browser",
                                      "url": "http://127.0.0.1:" +
                                             str(get_ufs_web_server_port()) +
                                             "/objsys/tagging_local/?" +
                                             links,
                                      "handle": "tagging"})


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    s = SimpleTagging()
    s.start_service()