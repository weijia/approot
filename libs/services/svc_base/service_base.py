# -*- coding: gbk -*-
from msg_service import *


class Service(object):
    def __init__(self, param_dict):
        #����һ��������̲߳�һ����Ҫinput����output����������worker�ĳ�ʼ���ı仯���������Ǵ�һ��param_dict������
        #Ȼ������Ҫʹ��input����output��ʱ���ٴ�param_dict�����ȡ��
        """
        param_dict���ܵĲ�����
        diagram_id
        session_id
        input_msg_q_name
        output
        """
        self.param_dict = param_dict
        super(Service, self).__init__()

        self.receiver = Receiver(self.get_input_msg_queue_name())
        self.is_stopped = False

    def add_item(self, param_dict):
        q = MsgQ(self.get_input_msg_queue_name())
        q.send(param_dict)

    def add_msg(self, msg):
        q = MsgQ(self.get_input_msg_queue_name())
        q.send_msg(msg)

    def get_session_id(self):
        return self.param_dict["session_id"]

    def get_input_msg_queue_name(self):
        return self.param_dict.get("input_msg_q_name", self.__class__.__name__ + "_default_input_msg_q_name")

    def startServer(self):
        '''
        For compatible with legacy simpleservice.py
        '''
        self.start_service()
        
    def start_service(self):
        self.receiver.register_to_data_msg_q()
        self.msg_loop()
        
        
    def msg_loop(self):
        while True:
            msg = self.receive()
            if msg.is_stop_msg():
                is_stopped = True
                self.stop()
            elif not self.process(msg):
                break
        #msg.set_processed()
        
    def process(self, msg):
        '''
        Process the received msg
        :param msg:
        :return: False: need to exit msg_loop
        '''
        pass
        
    def stop(self):
        pass