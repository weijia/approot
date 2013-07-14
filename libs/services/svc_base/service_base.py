# -*- coding: gbk -*-
import threading
from msg_service import *


class Service(object):
    def __init__(self, param_dict):
        #由于一个服务的线程不一定需要input或者output所以增加了worker的初始化的变化，因此最好是传一个param_dict进来，
        #然后再需要使用input或者output的时候再从param_dict里面获取。
        """
        param_dict可能的参数：
        diagram_id
        session_id
        input_msg_q_name
        output
        """
        self.param_dict = param_dict
        super(Service, self).__init__()
        self.is_stopped = False

    def add_task_info(self, msg):
        self.task_info = msg

    def get_output_msg_queue_name(self):
        return self.param_dict.get("output", None)

    def send_to_output(self, param_dict):
        """
        :param param_dict:
        :return:
        """
        """
        :param param_dict:
        :return:
        """
        q = MsgQ(self.get_output_msg_queue_name())
        q.send(param_dict)

    def addItem(self, item_dict):
        """
        Do not use this function
        This function is just used for compatible for legacy service
        :param item_dict:
        :return:
        """
        self.send_to_output(item_dict)

    def stop(self):
        """
        Called from external
        :return:
        """
        self.is_stopped = True

    def is_quitting(self):
        return self.is_stopped

    def get_session_id(self):
        return self.param_dict["session_id"]

    def on_stop(self):
        pass


class ThreadedService(Service, threading.Thread):
    def run(self):
        pass


class MsgProcessor(Service):
    """
    This class provides the basic message handling mechanism, it is not threaded. If thread for msg
    processing is needed, please use ThreadedMsgProcessor
    """
    def __init__(self, param_dict):
        super(MsgProcessor, self).__init__(param_dict)
        self.receiver = Receiver(self.get_input_msg_queue_name())

    def send_to_self(self, msg_dict):
        q = MsgQ(self.get_input_msg_queue_name())
        q.send(msg_dict)

    def put(self, msg_dict):
        """
        A quick function for send to self
        :param msg_dict:
        :return:
        """
        self.send_to_self(msg_dict)

    def add_msg(self, msg_dict):
        q = MsgQ(self.get_input_msg_queue_name())
        self.send_to_self(msg_dict)

    def receive(self):
        return self.receiver.receive()

    def get_input_msg_queue_name(self):
        return self.param_dict.get("input_msg_q_name", self.__class__.__name__ + "_default_input_msg_q_name")

    def startServer(self):
        """
        For compatible with legacy simpleservice.py
        """
        self.start_service()
        
    def start_service(self):
        self.receiver.register_to_data_msg_q()
        self.msg_loop()

    def msg_loop(self):
        while True:
            msg = self.receive()
            if msg.is_stop_msg():
                self.is_stopped = True
                self.on_stop()
            elif not self.process(msg):
                break
        #msg.set_processed()
        
    def process(self, msg):
        """
        Process the received msg
        :param msg:
        :return: False: need to exit msg_loop
        """
        pass



class ThreadedMsgProcessor(MsgProcessor, threading.Thread):
    def run(self):
        self.start_service()