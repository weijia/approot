# -*- coding: gbk -*-
import traceback
import beanstalkc
from configuration import g_config_dict
from msg import Msg
import libsys
from libs.logsys.logSys import *
import json

gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = g_config_dict["ufs_beanstalkd_port"]

DEFAULT_PRIORITY = beanstalkc.DEFAULT_PRIORITY
CMD_PRIORITY = 0


class MsgQueueNameIsNone: pass


class BeanstalkdMsgQ(object):
    def __init__(self, msg_q_name):
        if msg_q_name is None:
            raise MsgQueueNameIsNone
        self.msg_q_name = msg_q_name
        #self.beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)

    def send_cmd(self, msg_dict, delay=0):
        """
        delay is in seconds
        """
        #cl(msg_dict)
        self.send(msg_dict, priority=CMD_PRIORITY)

    def send(self, msg_dict, priority=DEFAULT_PRIORITY, delay=0):
        self.send_msg(Msg(msg_dict), priority, delay)

    def send_msg(self, msg, priority=DEFAULT_PRIORITY, delay=0):
        #ncl('port: ', gBeanstalkdServerPort)
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        try:
            beanstalk.use(self.msg_q_name)
        except:
            print 'using: "%s" failed', self.msg_q_name
        cl('sending to:', self.msg_q_name, msg)
        job = beanstalk.put(msg.to_json(), priority=priority, delay=delay)
        return job


class BeanstalkdReceiver(object):
    """
    """
    #如果采用不是指定timestamp放回消息队列，并且指令和数据使用同一个tube的话，会产生一个问题：
    #因为不能先从指令队列接收消息，所以可能会有很多数据队列的数据被接收
    #又由于会把这些数据消息放回消息队列，数据队列的顺序将被破坏
    def __init__(self, tube_name):
        self.tube_name = tube_name
        self.beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        self.cmd_tube_name = tube_name + "_cmd_tube"
        self.beanstalk.ignore('default')
        self.registered_to_cmd_tube = False

    #Command related msg queue registration
    def unregister_from_cmd_msg_q(self):
        self.beanstalk.ignore(self.get_cmd_msg_q_name())

    def register_to_cmd_msg_q(self):
        cl("watching: ", self.get_cmd_msg_q_name())
        self.beanstalk.watch(self.get_cmd_msg_q_name())

    def get_cmd_msg_q_name(self):
        return self.cmd_tube_name

    #Data related msg queue registration
    def unregister_from_data_msg_q(self):
        self.beanstalk.ignore(self.tube_name)
        self.registered_to_cmd_tube = False

    def register_to_data_msg_q(self):
        #self.registered_to_cmd_tube = True
        cl("watching: ", self.tube_name)
        self.beanstalk.watch(self.tube_name)

    #不能清空命令消息列表，因为本服务的其他实例可能已经在运行（或已经注册到服务管理器），
    #清空命令消息队列会导致另一个服务的服务消息被清空
    #def clean_cmd_q(self):
    #    pass

    def receive(self, timeout=None):
        try:
            #In beanstalkc lib, time is None means no timeout needed, so the call will be blocking.
            job = self.beanstalk.reserve(timeout)
        except:
            print 'receive exception, return from load_msg_without_exception'
            #self.stop()
            traceback.print_exc()
            raise
            #return None, None
        if job is None:
            return None
        msg = self.extract_msg_body(job)
        job.delete()
        return msg

    def extract_msg_body(self, job):
        item = json.loads(job.body)
        return Msg(item)

        # def receive_with_timestamp_from_cmd_q(self, timestamp):
        # '''
        # Receive msg with specific timestamp value
        # timestamp: expected timestamp
        # timeout: None. means no timeout needed, so the call is blocking.
        # Otherwise, this function will receive a msg until timetout. When timeout, this function will return None
        # '''
        # msg = self.receive(timeout)
        # if timestamp == msg.get_timestamp():
        # return msg
        # else:
        # MsgQ
            