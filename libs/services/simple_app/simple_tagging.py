from libtool import include_root_path
include_root_path(__file__, "approot")
import sys
print sys.path
import lib_list
from services.pyro_service.pyro_service_base import PyRoServiceBase
from services.svc_base.gui_client import GuiClient


class SimpleTagging(PyRoServiceBase):
    def __init__(self):
        super(SimpleTagging, self).__init__()
        self.gui_client = GuiClient()
        #Register to drop service. Service will create drop window and send the dropped items to tube
        receive_channel_name = "simple_tagging"
        self.gui_client.register_drop_msg_receiver(receive_channel_name, "simple_tagging")
        self.register(receive_channel_name)

    #########################
    # Called through pyro only
    #########################
    def put_msg(self, msg):
        print msg