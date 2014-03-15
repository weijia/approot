import logging
from libtool import include_root_path
include_root_path(__file__, "approot")
from config import get_ufs_web_server_port
from configuration import get_default_charset
from services.pyro_service.pyro_simple_app_base import PyroSimpleAppBase

from services.svc_base.gui_client import GuiClient
from utils.string_tools import SpecialEncoder

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
        s.start_service()
        self.close_drop_wnd()

    #########################
    # Called through pyro only
    #########################
    def put_msg(self, msg):
        links = ""
        e = SpecialEncoder()
        log.debug(msg)
        for i in msg["urls"]:
            links += "url=" + e.encode(unicode(i)).encode(get_default_charset()) + "&"
        self.gui_client.open_browser({"command": "Browser",
                                      "url": "http://127.0.0.1:" +
                                             str(get_ufs_web_server_port()) +
                                             "/objsys/tagging/?" +
                                             links + "encoding=" + get_default_charset(),
                                      "handle": "tagging"})


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    s = SimpleTagging()
    s.start_service()