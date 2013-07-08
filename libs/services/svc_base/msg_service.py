# -*- coding: gbk -*-

from beanstalkd_msg_service import BeanstalkdMsgQ
from beanstalkd_msg_service import BeanstalkdReceiver

#目前MsgQ是被假定为先进先出的，但是以后需要保持这种假设么？
MsgQ = BeanstalkdMsgQ
Receiver = BeanstalkdReceiver