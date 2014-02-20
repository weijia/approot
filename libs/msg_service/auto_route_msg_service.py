from msg_service.msg_service_interface import MsgServiceInterface, UnknownReceiver
from msg_service.pyro_msg_service import PyroMsgService


class AutoRouteMsgService(MsgServiceInterface):
    def __init__(self):
        super(AutoRouteMsgService, self).__init__()
        self.pyro_msg_service = PyroMsgService()

    def send_to(self, receiver, msg):
        try:
            self.pyro_msg_service.send_to(receiver, msg)
        except UnknownReceiver:
            pass