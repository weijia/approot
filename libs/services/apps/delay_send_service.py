# -*- coding: gbk -*- 
"""
Created on 2012-02-13

@author: Richard
"""
import os
import time
from libs.logsys.logSys import cl
import libsys
from libs.services.svc_base.simple_service_v2 import SimpleService
from libs.services.svc_base.managed_service import WorkerBase
import libs.utils.transform as transform

gDefaultDelaySeconds = 60 * 60


class DelaySendThread(WorkerBase):
    '''
    def __init__(self, input_tube, output_tube, timeout):
        """
        timeout is in seconds
        """
        super(DelaySendThread, self).__init__(input_tube)
        self.input_tube = input_tube
        self.output_tube = output_tube
    '''

    def add_task_info(self, msg):
        super(DelaySendThread, self).add_task_info(msg)
        #����Ҫ������ǰ�ύ����Ŀ���������timestamp���������ֵ���ͬ������Ŀ��
        self.timestamp = time.time()
        self.received_items = {}
        self.timeout = int(msg.get("timeout", gDefaultDelaySeconds))

    def process(self, msg):
        '''
        if self.output_tube is None:
            print 'error, no output tube given'
            #Do not put the item to target tube
            return False#Do not need to put the item back to the tube
        '''
        full_path = transform.format_path(msg.get_path())

        #Case 1, the item is first received no delay_send_timestamp
        #Add delay_send_timestamp and send with delay
        #Case 2, received the re-send item
        #If timestamp match, send, otherwise, ignore as there is another msg send
        #Case 3, received an item that is already stored
        #Add timestamp update time
        #������delay_timestamp�п��������������
        #   1.����Ŀ����ǰ���Ѿ��ύ��������task�����������У������µ�timestamp���ѵ�ǰtaskɾ����
        #   2.����Ŀ��û�ύ����        ����task�����������У������µ�timestamp���ѵ�ǰtaskɾ��
        #����delay_timestampҲ���������
        #   1.����Ŀ����ʱʱ�䵽����������task�����͵�output.�ѵ�ǰtaskɾ����
        #   2.����Ŀ����ʱʱ�䵽���ֺ����ָ��¹����������ѵ�ǰtaskɾ����

        #
        if self.timestamp != msg.get("delay_send_session_timestamp", 0):
            #Not put in tube in this session, update session timestamp and remove delay_send_timestamp
            msg["delay_send_session_timestamp"] = self.timestamp
            msg.pop("delay_send_timestamp", None)
            #Temp remove item
            #job.delete()
            #return False

        if "delay_send_timestamp" in msg:
            if self.received_items[full_path] == msg["delay_send_timestamp"]:
                #Item timeout, output it
                cl('timeout reached, send it:', msg, self.received_items[full_path], msg["delay_send_timestamp"])
                new_job = self.add_item(msg)
                del self.received_items[full_path]
            else:
                #Ignore the item
                pass
        else:
            new_timestamp = time.time()
            self.received_items[full_path] = new_timestamp
            msg.update({'delay_send_timestamp': new_timestamp, "delay_send_session_timestamp": self.timestamp})
            self.add_item(msg)
        return True


'''
class DelaySendService(beanstalkServiceApp):
    def processItem(self, job, item):
        input_tube = item["input"]
        output_tube = item["output"]
        timeout = item.get("timeout", gDefaultDelaySeconds)

        if self.is_processing_tube(input_tube):
            print 'input tube already processing'
            job.delete()
            return False#Do not need to put the item back to the tube
        t = DelaySendThread(input_tube, output_tube, timeout)
        self.add_work_thread(input_tube, t)
        t.start()
        job.delete()
        return False#Do not need to put the item back to the tube
'''

if __name__ == "__main__":
    s = SimpleService({"timeout": "Timeout value for processing", },
                      worker_thread_class=DelaySendThread)
    s.run()