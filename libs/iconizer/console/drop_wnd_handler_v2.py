from iconizer.console.drop_wnd_handler import DropWndHandler
from msg_service.auto_route_msg_service import AutoRouteMsgService


class DropWndHandlerV2(DropWndHandler):
    def handle(self, msg):
        if msg["command"] == "DropWndV2":
            target = msg["target"]
            tip = msg.get("tip", None)
            drop_wnd = self.gui_factory.create_drop_target(self.drop_callback)
            if not (tip is None):
                drop_wnd.label.setText(tip)
            self.wnd2target[drop_wnd] = target
            self.target2wnd[target] = drop_wnd
        elif msg["command"] == "DestroyDropWndV2":
            wnd = self.target2wnd[msg["target"]]
            del self.target2wnd[msg["target"]]
            del self.wnd2target[wnd]
            #del self.target2wnd[msg]
            wnd.deleteLater()

    def drop_callback(self, drop_wnd, urls):
        #print "dropped: ", urls
        #print drop_wnd, self.wnd2target
        target = self.wnd2target[drop_wnd]
        msg_service = AutoRouteMsgService()
        msg_service.send_to(target, {"command": "dropped", "urls": urls})