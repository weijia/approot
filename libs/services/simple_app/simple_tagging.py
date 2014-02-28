from libtool import include_root_path
include_root_path(__file__, "approot")
import lib_list
from services.pyro_service.pyro_service_base import PyRoServiceBase
from services.svc_base.gui_client import GuiClient
from libs.logsys.logSys import cl
from utils.string_tools import SpecialEncoder
from configuration import g_config_dict, get_default_charset


class SimpleTagging(PyRoServiceBase):
    def __init__(self):
        super(SimpleTagging, self).__init__()
        self.gui_client = GuiClient()
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.receive_channel_name = "simple_tagging"

    def open_drop_wnd(self):
        self.gui_client.register_drop_msg_receiver(self.receive_channel_name, "simple_tagging")

    def close_drop_wnd(self):
        self.gui_client.un_register_drop_msg_receiver(self.receive_channel_name)

    def start_service(self):
        self.register(self.receive_channel_name)

    #########################
    # Called through pyro only
    #########################
    def put_msg(self, msg):
        links = ""
        e = SpecialEncoder()
        cl(msg)
        for i in msg["urls"]:
            links += "url=" + e.encode(unicode(i)).encode(get_default_charset()) + "&"
        self.gui_client.open_browser({"command": "Browser",
                              "url": "http://127.0.0.1:" +
                                    str(g_config_dict["ufs_web_server_port"]) +
                                    "/objsys/tagging/?" +
                                    links + "encoding=" + get_default_charset(),
                              "handle": "tagging"})


if __name__ == "__main__":
    s = SimpleTagging()
    s.open_drop_wnd()
    s.start_service()
    s.close_drop_wnd()