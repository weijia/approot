from libs.services.svc_base.gui_service import GuiService
from libs.services.svc_base.msg_service import AutoRouteMsgService


class GuiClient(object):
    def __init__(self):
        self.msg_service = AutoRouteMsgService()

    def register_drop_msg_receiver(self, input_msg_queue_name, tip):
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.msg_service.sendto('system_gui_service_input_msg_q',
                                {"command": "DropWnd", "target":
                                    input_msg_queue_name, "tip": tip})

    def un_register_drop_msg_receiver(self, input_msg_queue_name):
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.msg_service.sendto('system_gui_service_input_msg_q',
                                {"command": "DestroyDropWnd",
                                 "target": input_msg_queue_name})