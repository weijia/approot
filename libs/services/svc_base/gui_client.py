import threading
from iconizer import Iconizer
from iconizer.iconizer_consts import ICONIZER_SERVICE_NAME
from msg_service.auto_route_msg_service import AutoRouteMsgService


class GuiClient(object):
    def __init__(self):
        self.msg_service = AutoRouteMsgService()

    def register_drop_msg_receiver(self, input_msg_queue_name, tip):
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.msg_service.send_to(ICONIZER_SERVICE_NAME,
                                {"command": "DropWnd", "target":
                                    input_msg_queue_name, "tip": tip})

    def un_register_drop_msg_receiver(self, input_msg_queue_name):
        #Register to drop service. Service will create drop window and send the dropped items to tube
        self.msg_service.send_to(ICONIZER_SERVICE_NAME,
                                {"command": "DestroyDropWnd",
                                 "target": input_msg_queue_name})


if __name__ == "__main__":
    class OpenDropWndThread(threading.Thread):
        def run(self):
            import time
            time.sleep(10)
            GuiClient().register_drop_msg_receiver("good", "hello world")

    OpenDropWndThread().start()
    Iconizer().execute({"": ["dir"]})