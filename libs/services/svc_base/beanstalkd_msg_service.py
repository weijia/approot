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
    #������ò���ָ��timestamp�Ż���Ϣ���У�����ָ�������ʹ��ͬһ��tube�Ļ��������һ�����⣺
    #��Ϊ�����ȴ�ָ����н�����Ϣ�����Կ��ܻ��кܶ����ݶ��е����ݱ�����
    #�����ڻ����Щ������Ϣ�Ż���Ϣ���У����ݶ��е�˳�򽫱��ƻ�
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

    #�������������Ϣ�б���Ϊ�����������ʵ�������Ѿ������У����Ѿ�ע�ᵽ�������������
    #���������Ϣ���лᵼ����һ������ķ�����Ϣ�����
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
            