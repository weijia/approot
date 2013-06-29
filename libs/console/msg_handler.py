
import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkServiceBase



class GuiServiceMsgHandler(object):
    def __init__(self, gui_factory):
        super(GuiServiceMsgHandler, self).__init__()
        self.gui_factory = gui_factory
        self.wnd2target = {}
        self.handle2browser = {}
    def handle_msg(self, msg):
        if msg["command"] == "DropWnd":
            target = msg["target"]
            drop_wnd = self.gui_factory.create_drop_target(self.drop_callback)
            self.wnd2target[drop_wnd] = target
        if msg["command"] == "Browser":
            url = msg["url"]
            handle = msg["handle"]
            self.gui_factory.show_browser(handle, url)
        if msg["command"] == "notify":
            msg_str = msg["msg"]
            self.gui_factory.msg(msg_str)
        

    def drop_callback(self, drop_wnd, urls):
        print "dropped: ", urls
        target = self.wnd2target[drop_wnd]
        target_queue = beanstalkServiceBase(target)
        #for i in urls:
        target_queue.put({"command": "dropped", "urls": urls})