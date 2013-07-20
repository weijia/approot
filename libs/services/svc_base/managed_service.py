# -*- coding: gbk -*-
import os
import time
import threading
from libs.services.svc_base.service_base import MsgProcessor
from libs.services.svc_base.msg import RegMsg
from libs.services.svc_base.msg_service import *
from libs.services.svc_base.diagram_state import DiagramState
from libs.services.svc_base.msg_based_service_mgr import gMsgBasedServiceManagerMsgQName
from libs.logsys.logSys import *
from libs.utils.filetools import get_main_file


class ManagedService(MsgProcessor):
    """
    ManagedService will be managed from MsgBasedServiceManager through message.
    """
    WAIT_FOR_REGISTRATION_DONE_TIMEOUT = 20
    RETRY_FOR_REGISTRATION_DONE = 10

    def __init__(self, param_dict):
        #���ܻ���һ����������msg queue
        #����Ҫ��һ��cmd msg queue�����տ�����Ϣ
        super(ManagedService, self).__init__(param_dict)
        self.output = None
        cl(self.param_dict)
        #if not (self.param_dict.get("output", None) is None):
        #    self.output = MsgQ(self.get_output_msg_queue_name())
        self.state = None
        if "diagram_id" in param_dict:
            self.state = DiagramState(param_dict["diagram_id"])

    def get_task_signature(self):
        #import __main__
        #cl(dir(__main__))
        #cl(__main__.__name__)
        #try:
        #    cl(__main__.__file__)
        #except:
        #    pass
        #print "exe filename:", __main__.__file__
        app_name = get_main_file()
        return app_name

    def register_service(self):
        msg = RegMsg()
        msg.add_app_name(self.get_task_signature())
        msg.add_receiver(self.receiver)
        msg.add_timestamp()
        msg.add_session_id(self.param_dict.get("session_id"))
        self.reg_timestamp = msg.get_timestamp()
        q = MsgQ(gMsgBasedServiceManagerMsgQName)
        q.send_msg(msg)

    def receive_register_ok(self):
        self.receiver.register_to_cmd_msg_q()
        for retry_cnt in range(0, self.RETRY_FOR_REGISTRATION_DONE):
            msg = self.receive(timeout=self.WAIT_FOR_REGISTRATION_DONE_TIMEOUT)
            if msg is None:
                print 'receive msg error, retry...', self.get_input_msg_queue_name()
                ###################
                # Receive failed, quiting
                continue

            #Every control msg must have a timestamp
            if not ('timestamp' in msg):
                cl('no timestamp, drop msg')
                continue
            if msg["timestamp"] + 20 < time.time():
                ###################
                #Very old control msg, ignore it
                cl("Very old control msg, drop it", msg)
                continue

            put_delay = 2   # In seconds
            #Only care about pid matched message
            if (msg.is_pid_match()) and (self.reg_timestamp == msg.get("timestamp", 0)):
                reg_msg = RegMsg(msg)
                if reg_msg.is_registration_ok():
                    #It is the master service app, shall be responsible for clean stop msg is there is some
                    cl('Register OK')
                    return True
                else:
                    cl('Registration failed')
                    ###################
                    # Receive failed, quiting
                    return False
            else:
                #Put the msg back as we are not the target for this command
                #This is not a register msg, put it back
                q = MsgQ(self.receiver.get_cmd_msg_q_name())
                q.send_cmd(msg)
                #TODO: maybe should sleep random seconds
                time.sleep(1)
                cl("msg sent back, back to msg loop")

        #All retry failed, quit this task
        return False

    def start_service(self):
        #ע�ᵽ������Ϣ֮ǰҪ�ж��Ƿ���յ�ǰsession�������Ϣ��
        #��Ϊ���������Ϣ��ʱ��û������cmd��data msg queue������ֻ��session�жϣ�����cmd���ر�ı��ʹ��cmd��Ϣ�ܸ�
        #data��Ϣ������
        #���cmd��Ϣ����
        #receiver.clear(self.get_input_msg_queue_name())
        #ע�ᵽcmd��Ϣ����

        #ͨ��cmd��Ϣ����ע�ᵽ����������
        self.register_service()
        if self.receive_register_ok():
            #ע�ᵽdata��Ϣ����
            self.receiver.register_to_data_msg_q()
            #��ʼ��Ϣѭ��������Ϣ
            self.msg_loop()


class WorkerBase(ManagedService, threading.Thread):
    def __init__(self, param_dict):
        super(WorkerBase, self).__init__(param_dict)
        #cl(param_dict)
        #cl(param_dict.get("output", "no_output"))
        #������¼���ڴ����һ���ӷ������յ�����Ϣ��timestamp��������������⵽�����Ѿ��ڴ������һ����Ϣ
        #����Լ�����worker�����µ���Ϣ
        self.last_timestamp = 0
        self.worker_init()

    def worker_init(self):
        cl("calling worker init in worker base")
        pass

    def get_last_processing_timestamp(self):
        return self.last_timestamp

    def get_task_signature(self):
        app_name = super(WorkerBase, self).get_task_signature()
        service_msg_q_name = super(WorkerBase, self).get_input_msg_queue_name()
        signature = "%s:worker:%s" % (service_msg_q_name,
                                      self.get_output_msg_queue_name())
        return signature

    def run(self):
        self.start_service()
    '''
    # The MsgProcessor will use "input" and "output" param as input queue so we do not
    # need to override this func to set different worker input here
    def get_input_msg_queue_name(self):
        super(WorkerBase, self).get_input_msg_queue_name()
    '''