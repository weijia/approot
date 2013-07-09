# -*- coding: gbk -*-
import os
from service_base import Service
from msg import RegMsg
from msg_service import *
import threading
from diagram_state import DiagramState
from msg_based_service_mgr import gMsgBasedServiceManagerMsgQName
        
class ManagedService(Service):
    def __init__(self, param_dict):
        '''
        可能会有一个数据输入msg queue
        必须要有一个cmd msg queue来接收控制消息
        '''
        super(ManagedService, self).__init__(param_dict)
        self.output = None
        if param_dict.has_key("output"):
            self.output = MsgQ(param_dict["output"])
        self.state = None
        if param_dict.has_ley("diagram_id"):
            self.state = DiagramState(param_dict["diagram_id"])

    # def receive(self):
        # '''
        # blocking call that will be overrided by Receiver.
        # '''
        # pass
    
    def register_service(self):
        msg = RegMsg()
        import __main__
        #print "exe filename:", __main__.__file__
        app_name = os.path.basename(__main__.__file__).split(".")[0]
        msg.add_app_name(app_name)
        msg.add_receiver(self.receiver)
        msg.add_timestamp()
        q = MsgQ(gMsgBasedServiceManagerMsgQName)
        q.send(msg)
                
                
    WAIT_FOR_REGISTRATION_DONE_TIMEOUT = 20
    RETRY_FOR_REGISTRATION_DONE = 10
                
    def receive_register_ok(self, timestamp):
        self.receiver.register_to_cmd_msg_q()
        for retry_cnt in range(0, self.RETRY_FOR_REGISTRATION_DONE):
            msg = self.receiver.receive(timeout=self.WAIT_FOR_REGISTRATION_DONE_TIMEOUT)
            if msg is None:
                print 'receive msg error, retry...', self.get_input_tube_name()
                ###################
                # Receive failed, quiting
                continue
                
            #Every control msg must have a timestamp
            if not msg.has_key('timestamp'):
                cl('no timestamp, drop msg')
                continue
            if msg["timestamp"] + 20 < time.time():
                ###################
                #Very old control msg, ignore it
                cl("Very old control msg, drop it", msg)
                continue
                
            put_delay = 2#In seconds
            #Only care about pid matched message
            if msg.get("pid", 0) == self.pid:
                if msg.has_key("cmd"):
                    if msg["cmd"] == "tube_already_registered":
                        cl('duplicated service register signal received, quit this one')
                        ###################
                        # Receive failed, quiting
                        return False
                    elif msg["cmd"] == "register_ok":
                        #It is the master service app, shall be responsible for clean stop msg is there is some
                        cl('register OK')
                        return True
                        
            #Put the msg back as we are not the target for this command
            #This is not a register msg, put it back
            q = MsgQ(receiver.get_cmd_msg_q_name())
            q.send_cmd(msg)
            cl("msg sent back, back to msg loop")
        
        #All retry failed, quit this task
        return False

    
    def start_service(self):
        #注册到接收消息之前要判断是否接收当前session以外的消息。
        #因为任务接收消息的时候没有区分cmd和data msg queue，不能只用session判断，除非cmd有特别的标记使得cmd消息能跟
        #data消息区别开来
        #清空cmd消息队列
        #receiver.clear(self.get_input_msg_queue_name())
        #注册到cmd消息队列
        
        #通过cmd消息队列注册到服务管理程序
        self.register_service()
        if self.receive_register_ok():
            #注册到data消息队列
            self.register_to_data_msg_q()
            #开始消息循环处理消息
            self.msg_loop()
        
            
class WorkerBase(ManagedService, threading.Thread):
    def __init__(self, param_dict):
        super(WorkerBase, self).__init__(param_dict)
        #用来记录正在处理的一条从服务器收到的消息的timestamp，这样服务器检测到进程已经在处理最后一条消息
        #则可以继续给worker发送新的消息
        self.last_timestamp = 0

    def get_last_processing_timestamp(self):
        return self.last_timestamp
        
