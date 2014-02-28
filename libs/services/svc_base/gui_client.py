from iconizer.iconizer_consts import ICONIZER_SERVICE_NAME
from msg_service.auto_route_msg_service import AutoRouteMsgService


class GuiClient(object):
    def __init__(self):
        self.msg_service = AutoRouteMsgService()

    def register_drop_msg_receiver(self, target, tip):
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.msg_service.send_to(ICONIZER_SERVICE_NAME,
                                 {"command": "DropWndV2", "target":
                                     target, "tip": tip})

    def un_register_drop_msg_receiver(self, target):
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.msg_service.send_to(ICONIZER_SERVICE_NAME,
                                 {"command": "DestroyDropWndV2",
                                  "target": target})

    def open_browser(self, msg):
        self.msg_service.send_to(ICONIZER_SERVICE_NAME, msg)