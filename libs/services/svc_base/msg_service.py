# -*- coding: gbk -*-
import Pyro4

from beanstalkd_msg_service import BeanstalkdMsgQ
from beanstalkd_msg_service import BeanstalkdReceiver

#目前MsgQ是被假定为先进先出的，但是以后需要保持这种假设么？
MsgQ = BeanstalkdMsgQ
Receiver = BeanstalkdReceiver


class MsgServiceInterface(object):
    def sendto(self, receiver_name, msg):
        pass

    def receive_from_blocking(self, msg_queue):
        pass


class Pyro4MsgService(MsgServiceInterface):
    def sendto(self, receiver_name, msg):
        name_server = Pyro4.locateNS()
        proxy_uri = name_server.lookup("receiver_name")
        proxy = Pyro4.Proxy(proxy_uri)
        proxy.send_msg(msg)

    def receive_from_blocking(self):
        pass


class AutoRouteMsgService(MsgServiceInterface):
    def sendto(self, receiver_name, msg):
        if receiver_name == 'system_gui_service_input_msg_q':
            name_server = Pyro4.locateNS()
            proxy_uri = name_server.lookup("ufs_launcher")
            proxy = Pyro4.Proxy(proxy_uri)
            proxy.send_msg(msg)

    def receive_from_blocking(self, msg_queue):
        pass