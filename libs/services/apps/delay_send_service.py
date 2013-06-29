# -*- coding: gbk -*- 
'''
Created on 2012-02-13

@author: Richard
'''
import os
import time
import beanstalkc
import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread, beanstalkServiceApp
import libs.utils.simplejson as json
import libs.utils.transform as transform 
from libs.services.svc_base.simpleservice import SimpleService


class DelaySendThread(beanstalkWorkingThread):
    def __init__(self, input_tube, output_tube, timeout):
        '''
        timeout is in seconds
        '''
        super(DelaySendThread, self).__init__(input_tube)
        self.input_tube = input_tube
        self.output_tube = output_tube
        self.timeout = int(timeout)
        self.received_items = {}
        #����Ҫ������ǰ�ύ����Ŀ���������timestamp���������ֵ���ͬ������Ŀ��
        self.timestamp = time.time()
        
    def processItem(self, job, item):
        if self.output_tube is None:
            print 'error, no output tube given'
            #Do not put the item to target tube
            job.delete()
            return False#Do not need to put the item back to the tube
            
        full_path = transform.transformDirToInternal(item["fullpath"])

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
        if self.timestamp != item.get("delay_send_session_timestamp", 0):
            #Not put in tube in this session, update session timestamp and remove delay_send_timestamp
            item["delay_send_session_timestamp"] = self.timestamp
            item.pop("delay_send_timestamp", None)
            #Temp remove item
            #job.delete()
            #return False
        
        
        if item.has_key("delay_send_timestamp"):
            if self.received_items[full_path] == item["delay_send_timestamp"]:
                #Item timeout, output it
                print 'timeout reached, send it:', item, self.received_items[full_path], item["delay_send_timestamp"]
                new_job = self.put_item(item, self.output_tube)
                del self.received_items[full_path]
            else:
                #Ignore the item
                pass
        else:
            new_timestamp = time.time()
            self.received_items[full_path] = new_timestamp
            item.update({'delay_send_timestamp': new_timestamp, "delay_send_session_timestamp": self.timestamp})
            self.put(item, delay = self.timeout)
            

        job.delete()        
        return False#Do not need to put the item back to the tube

gDefaultDelaySeconds = 60*60

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


    
    
        
if __name__ == "__main__":
    s = SimpleService({
                            "input": "Input tube for generator",
                            "output": "Output tube for generator",
                            "timeout": "Timeout value for processing",
                      },
                      DelaySendService)
    s.run()