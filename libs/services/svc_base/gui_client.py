from libs.services.svc_base.gui_service import GuiService


class GuiClient(object):
    def __init__(self):
        self.gui_service = GuiService()

    def register_drop_msg_receiver(self, input_msg_queue_name, tip):
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.gui_service.put({"command": "DropWnd", "target": input_msg_queue_name,
                              "tip": tip})

    def un_register_drop_msg_receiver(self, input_msg_queue_name):
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.gui_service.put({"command": "DestroyDropWnd",
                              "target": input_msg_queue_name})