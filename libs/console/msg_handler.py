import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkServiceBase


class GuiServiceMsgHandler(object):
    def __init__(self, gui_factory):
        super(GuiServiceMsgHandler, self).__init__()
        self.gui_factory = gui_factory
        self.wnd2target = {}
        self.target2wnd = {}
        self.handle2browser = {}

    def handle_msg(self, msg):
        if msg["command"] == "DropWnd":
            target = msg["target"]
            tip = msg.get("tip", None)
            drop_wnd = self.gui_factory.create_drop_target(self.drop_callback)
            if not (tip is None):
                drop_wnd.label.setText(tip)
            self.wnd2target[drop_wnd] = target
            self.target2wnd[target] = drop_wnd
        if msg["command"] == "DestroyDropWnd":
            wnd = self.target2wnd[msg["target"]]
            del self.target2wnd[msg["target"]]
            del self.wnd2target[wnd]
            #del self.target2wnd[msg]
            wnd.deleteLater()
        if msg["command"] == "Browser":
            url = msg["url"]
            handle = msg["handle"]
            self.gui_factory.show_browser(handle, url)
        if msg["command"] == "notify":
            msg_str = msg["msg"]
            self.gui_factory.msg(msg_str)

    def drop_callback(self, drop_wnd, urls):
        #print "dropped: ", urls
        #print drop_wnd, self.wnd2target
        target = self.wnd2target[drop_wnd]
        target_queue = beanstalkServiceBase(target)
        #for i in urls:
        target_queue.put({"command": "dropped", "urls": urls})