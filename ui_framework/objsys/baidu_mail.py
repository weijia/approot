# -*- coding: utf-8 -*-
from bae.core import const
from bae.api.bcms import BaeBcms
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address


class EmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        bcms = BaeBcms(const.ACCESS_KEY, const.SECRET_KEY)
        
        ### 创建queue
        ret = bcms.createQueue("myqueue1")
     
        ### 获取real qname
        real_qname = str(ret['response_params']['queue_name'])
        
        for email_message in email_messages:
            ### 发送邮件
            from_email = sanitize_address(email_message.from_email, email_message.encoding)
            recipients = [sanitize_address(addr, email_message.encoding)
                          for addr in email_message.recipients()]

            ret = bcms.mail(real_qname, email_message.message().as_string(), recipients, from_email, "你好，这是一封书签服务帐号激活邮件")
         
        ### 删除queue
        ret = bcms.dropQueue(real_qname)
        return len(email_messages)
 
def bcms_test():
    bcms = BaeBcms(const.ACCESS_KEY, const.SECRET_KEY)
 
    ### 创建queue
    ret = bcms.createQueue("myqueue1")
 
    ### 获取real qname
    real_qname = str(ret['response_params']['queue_name'])
 
    msg1 = "hello bcms"
    msg2 = u"你好BCMS"
 
    ### 发送消息
    ret = bcms.publishMessage(real_qname, msg1)
    msgid1 = ret['response_params']['msg_id']
 
    ret = bcms.publishMessage(real_qname, msg2)
    msgid2 = ret['response_params']['msg_id']
 
 
    ### 获取消息
    ret = bcms.fetchMessage(real_qname, fetch_num=10)['response_params']
    msgnum = ret['message_num']
    assert msgnum == 2
    msg_list = ret['messages']
    m1 = msg_list[0]
    assert m1['msg_id'] == msgid1
    assert m1['message_length'] == len(msg1)
    assert m1['message'] == msg1
    m2 = msg_list[1]
    assert m2['msg_id'] == msgid2
    #assert m2['message_length'] == len(msg2)
    assert m2['message'] == msg2
 
    ### 删除消息
    ret = bcms.deleteMessageById(real_qname, msgid1)
    ret = bcms.deleteMessageById(real_qname, msgid2)
 
    ### 发送邮件
    to = ["xxx@lalala.com"]
    ret = bcms.mail(real_qname, "你好，我们是BAE", to, "support@baidu.com",
"hello from BAE")
 
    ### 删除queue
    ret = bcms.dropQueue(real_qname)