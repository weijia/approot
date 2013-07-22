# -*- coding: gbk -*-
import threading
from libs.logsys.logSys import cl
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
        self.is_stopped = False

    def add_task_info(self, msg):
        cl("adding task_info: ", msg)
        self.task_info = msg

    def get_task_info(self):
        return self.task_info

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
        """
        This will be called when framework is stopping, just like window close event.
        Processor should return False if it don't want to quit at once.
        """
        return True

    def is_server_only(self):
        """
        Used for SimpleService to determine if it will be used to create tasks
        """
        return False


class ThreadedService(Service, threading.Thread):
    def run(self):
        pass


class MsgProcessor(Service):
    """
    This class provides the basic message handling mechanism, it is not threaded. If thread for msg
    processing is needed, please use ThreadedMsgProcessor

    Service default data input msg queue name: service class name + "_default_input_msg_q_name"

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

    def is_ignoring_legacy_session_msg(self, msg):
        if msg.get_session_id() != self.param_dict["session_id"]:
            print "ignore legacy session msg", msg, self.param_dict["session_id"]
            return True
        return False

    def add_msg(self, msg_dict):
        q = MsgQ(self.get_input_msg_queue_name())
        self.send_to_self(msg_dict)

    def receive(self, timeout=None):
        return self.receiver.receive(timeout)

    def get_input_msg_queue_name(self):
        """
        This function will use "input" param so child class need not override this function
        :return:
        """
        #cl(self.param_dict.get("output", "no_output"))
        #As output may be None value, we have to check the None state here
        output_msg_q_name = self.param_dict.get("output", None)
        if output_msg_q_name is None:
            output_msg_q_name = "no_input"
        cl("receiving from:", self.param_dict.get("input",
                                                  self.__class__.__name__ +
                                                  "_default_input_msg_q_name_with_output" +
                                                  output_msg_q_name
        ))
        return self.param_dict.get("input",
                                   self.__class__.__name__ +
                                   "_default_input_msg_q_name_with_output" +
                                   output_msg_q_name)

    def startServer(self):
        """
        For compatible with legacy simpleservice.py
        """
        self.start_service()

    def start_service(self):
        self.receiver.register_to_data_msg_q()
        self.msg_loop()

    def handle_cmd(self, msg):
        pass

    def internal_do_quit(self):
        """
        Call on_stop, if app does not want to quit directly, it should override on_stop and return False
        If app do not want to do any clean up stuff, just return True to let service stop.
        :return:
        """
        self.is_stopped = self.on_stop()

    def msg_loop(self):
        """
        This function will loop to receive message. The following messages will be handled in this level:
        stop message: {"cmd": "stop"}, stop the message loop
        #The following is not needed as we know all diagram's message queue. Because the message queue is generated
        #using a fixed schema. We can send stop to all message queues.
        #The above is not correct as some service may not have message queue.
        stop_diagram: {"cmd": "stop_diagram"}, stop the task for the specified diagram
        :return:
        """
        while not self.is_stopped:
            msg = self.receive()
            if msg.is_cmd():
                if msg.is_stop_msg():
                    self.internal_do_quit()
                else:
                    self.handle_cmd(msg)
            elif not self.process_msg_with_exception_captured(msg):
                break
                #msg.set_processed()
        print "quitting message loop"

    def process_msg_with_exception_captured(self, msg):
        try:
            return self.process(msg)
        except:
            print "process exception captured, msg:", msg
            import traceback
            traceback.print_exc()
        return True   # Do not quit if we got exception

    def process(self, msg):
        """
        Process the received msg,default operation is to discard message from other sessions
        :param msg:
        :return: False: need to exit msg_loop
        """
        if msg.get_session_id() == self.param_dict.get("session_id", 0):
            return self.process_cur_session_msg(msg)
        return True

    def process_cur_session_msg(self, msg):
        pass


class ThreadedMsgProcessor(MsgProcessor, threading.Thread):
    def run(self):
        self.start_service()