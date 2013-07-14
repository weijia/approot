import libsys
from libs.services.svc_base.service_base import ThreadedMsgProcessor


class GuiService(ThreadedMsgProcessor):
    def __init__(self, gui_factory=None):
        super(GuiService, self).__init__({"input_msg_q_name": "system_gui_service_input_msg_q"})
        #threading.Thread.__init__(self)
        self.gui_factory = gui_factory

    def process(self, msg):
        self.gui_factory.trigger(msg)
        return True

    def gui_msg(self, s):
        self.send_to_self({"command": "notify", "msg": s})