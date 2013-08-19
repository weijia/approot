# -*- coding: gbk -*-
import libsys
from libs.services.svc_base.launcher import Launcher
from libs.services.svc_base.gui_service import GuiService
from libs.services.svc_base.msg_service import MsgQ
from libs.services.svc_base.service_base import MsgProcessor
from libs.logsys.logSys import *
from libs.services.svc_base.msg import RegMsg, Msg, UnRegMsg
import argparse

gMsgBasedServiceManagerMsgQName = "msg_based_service_manager_msg_queue_name"


class MsgBasedServiceManager(MsgProcessor):
    def __init__(self, param_dict):
        param_dict["input"] = gMsgBasedServiceManagerMsgQName
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

    def handle_unregistration(self, msg):
        if self.get_session_id() != msg.get_session_id():
            print "Received a registration request for legacy session, ignore it"
        else:
            unreg_msg = UnRegMsg(msg)
            if unreg_msg.is_valid():
                if unreg_msg.get_app_name() in self.app_name_to_info:
                    del self.app_name_to_info[unreg_msg.get_app_name()]
                    unreg_msg.set_unregistration_result(True)
                    cl("App unregister success: %s" % unreg_msg.get_app_name())
                else:
                    cl("App not registered: %s" % msg.get_app_name())
                    unreg_msg.set_unregistration_result(False)
                MsgQ(msg.get_cmd_q_name()).send_cmd(unreg_msg)
            else:
                print "invalid unregistration msg"

    def msg_loop(self):
        while True:
            msg = self.receiver.receive()
            #print msg
            if self.is_ignoring_legacy_session_msg(msg):
                continue
            if not self.process(msg):
                break
        cl('quiting msg based service manager')

    def broadcast_cmd_msg(self, msg):
        for app_name in self.app_name_to_info:
            MsgQ(self.app_name_to_info[app_name].get_cmd_q_name()).send_cmd(msg)
        return True

    def process(self, msg):
        cl(msg)
        is_not_quit = True
        if "cmd" in msg:
            if msg["cmd"] == "registration":
                self.handle_registration(msg)
            elif msg["cmd"] == "unregistration":
                self.handle_unregistration(msg)
            elif msg["cmd"] == "start":
                #Start an app if not started
                if msg.has_app_name():
                    if msg.get_app_name() in self.app_name_to_info:
                        print "Unneeded start app, app already started"
                    else:
                        Launcher().start_app_with_name_param_list_with_session_no_wait(msg.get_app_name(),
                                                                                       ['--startserver'])
            elif msg["cmd"] == "broadcast_cmd":
                #Broadcast a message to all managed service
                self.broadcast_cmd_msg(msg)
            elif msg.is_stop_msg():
                stop_msg = Msg()
                stop_msg.add_cmd("stop")
                self.broadcast_cmd_msg(stop_msg)
                is_not_quit = False   # Break from message loop
            else:
                cl("Unexpected command:", msg)
        return is_not_quit


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--session_id", help="the session id for all processors in one diagram is unique," +
                                             "so processors can identify legacy data in tubes using this")
    args = vars(parser.parse_args())
    s = MsgBasedServiceManager({"session_id": args["session_id"]})
    s.start_service()