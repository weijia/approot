

class DropWndHandler(object):
    def __init__(self, gui_factory):
        super(DropWndHandler, self).__init__()
        self.gui_factory = gui_factory

    def handle(self, msg):
        if msg["command"] == "DropWnd":
            target = msg["target"]
            tip = msg.get("tip", None)
            drop_wnd = self.gui_factory.create_drop_target(self.drop_callback)
            if not (tip is None):
                drop_wnd.label.setText(tip)
            self.wnd2target[drop_wnd] = target
            self.target2wnd[target] = drop_wnd
        elif msg["command"] == "DestroyDropWnd":
            wnd = self.target2wnd[msg["target"]]
            del self.target2wnd[msg["target"]]
            del self.wnd2target[wnd]
            #del self.target2wnd[msg]
            wnd.deleteLater()

    def drop_callback(self, drop_wnd, urls):
        #print "dropped: ", urls
        #print drop_wnd, self.wnd2target
        target = self.wnd2target[drop_wnd]
        #target_queue = beanstalkServiceBase(target)
        if not (self.gui_launch_manger.msg_service is None):
            try:
                self.gui_launch_manger.msg_service.sendto(target, {"command": "dropped", "urls": urls})
            except:
                import traceback
                traceback.print_exc()