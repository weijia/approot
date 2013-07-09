# -*- coding: gbk -*-
from libs.services.svc_base.gui_service import GuiService
from libs.services.svc_base.msg_service import MsgQ
from service_base import Service
from libs.logsys.logSys import *
from msg import RegMsg, Msg

gMsgBasedServiceManagerMsgQName = "msg_based_service_manager_msg_queue_name"


class MsgBasedServiceManager(Service):
    def __init__(self, param_dict):
        super(MsgBasedServiceManager, self).__init__(param_dict)
        self.app_name_to_info = {}

    def handle_registration(self, msg):
        #Keep app name, pid, session, input cmd queue name
        if self.get_session_id() != msg.get_session_id():
            print "Received a registration request for legacy session, ignore it"
        else:
            reg_msg = RegMsg(msg)
            if reg_msg.is_valid():
                if reg_msg.get_app_name() in self.app_name_to_info:
                    print "Duplicated registration, app already started"
                    reg_msg.set_registration_result(False)
                else:
                    self.app_name_to_info[reg_msg.get_app_name()] = reg_msg
                    reg_msg.set_registration_result(True)
                MsgQ(msg.get_cmd_q_name()).send_cmd(reg_msg)
            else:
                print "invalid registration msg"
        return True

    def process(self, msg):
        if msg.is_stop_msg():
            #Send stop msg to all registered services
            return False
        
        if "cmd" in msg:
            if msg["cmd"] == "registration":
                return self.handle_registration(msg)
            elif msg["cmd"] == "start":
                #Start an app if not started
                if msg.has_app_name():
                    if msg.get_app_name() in self.app_name_to_info:
                        print "Unneeded start app, app already started"
                    else:
                        gui_service = GuiService()
                        gui_service.addItem({"command": "LaunchApp", "app_name": msg.get_app_name(), "param":['--startserver']})
            elif msg["cmd"] == "stop":
                for app_name in self.app_name_to_info:
                    MsgQ(self.app_name_to_info[app_name].get_cmd_q_name()).send_cmd(Msg().add_cmd("stop"))
            else:
                cl("Unexpected command")


if __name__ == "__main__":
    s = MsgBasedServiceManager({"input_msg_q_name": gMsgBasedServiceManagerMsgQName})
    s.start_service()