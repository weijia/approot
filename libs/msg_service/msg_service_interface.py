

class UnknownReceiver(Exception):
    pass


class MsgServiceInterface(object):
    def send_to(self, receiver, msg):
        pass
