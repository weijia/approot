# -*- coding: gbk -*-
from msg_service import *

class Service(object):
    def __init__(self, param_dict):
        '''
        ����һ��������̲߳�һ����Ҫinput����output����������worker�ĳ�ʼ���ı仯���������Ǵ�һ��param_dict������
        Ȼ������Ҫʹ��input����output��ʱ���ٴ�param_dict�����ȡ�����ܵĲ�����
        diagram_id
        session_id
        input_msg_q_name
        output
        '''
        self.param_dict = param_dict
        super(Service, self).__init__()
        '''
        self.diagram_id = diagram_id
        self.session_id = session_id
        if not (input_msg_q is None):
            self.input = MsgQ(input_msg_q)
        if not (output_msg_q is None):
            self.output = MsgQ(output_msg_q)
        '''
        self.receiver = Receiver(self.get_input_msg_queue_name())
        
    def get_input_msg_queue_name(self):
        self.param_dict.get("input_msg_q_name", self.__class__.__name__ + "_default_input_msg_q_name")

    def startServer(self):
        '''
        For compatitable with legacy simpleservice.py
        '''
        self.start_service()
        
    def start_service(self):
        self.receiver.register_to_data_q()
        self.msg_loop()
        
        
    def msg_loop(self):
        while True:
            msg = self.receive()
            if not self.process(msg):
                break
        #msg.set_processed()
        
    def process(self, msg):
        pass
        
    #def stop(self):
    #    pass