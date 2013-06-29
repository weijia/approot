'''
Created on 2012-02-13

@author: Richard
'''
#import os
import time
import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread, beanstalkServiceApp
from libs.services.svc_base.simpleservice import SimpleService


class ReSendThread(beanstalkWorkingThread):
    def __init__(self, input_tube, output_tube, timeout):
        '''
        timeout is in seconds
        '''
        super(ReSendThread, self).__init__(input_tube)
        self.input_tube = input_tube
        self.output_tube = output_tube
        self.timeout = timeout
        #Only item for this session will be processed. So timestamp other than the following will be ignored
        self.timestamp = time.time()
        
    def processItem(self, job, item):
        if self.output_tube is None:
            print 'error, no output tube given'
            #Do not put the item to target tube
            job.delete()
            return False#Do not need to put the item back to the tube
        #The following has problem. release the jog does not update item. So we must put a new object with updated attributes
        #job.release(delay=self.timeout)
        resend_cnt = item.get("resend_cnt", 0)
        item["resend_cnt"] = resend_cnt + 1
        if item.has_key('resend_session_timestamp'):
            if item['resend_session_timestamp'] != self.timestamp:
                #Not created by this re-send session
                job.delete()
                return False
        else:
            item["resend_session_timestamp"] = self.timestamp
            
        new_job = self.put_item(item, self.output_tube)
        self.put(item, delay=self.timeout)
        return False#Do not need to put the item back to the tube



class ReSendService(beanstalkServiceApp):
    def processItem(self, job, item):
        input_tube = item["input"]
        output_tube = item["output"]
        timeout = item.get("timeout", 60*60)

        if self.is_processing_tube(input_tube):
            print 'input tube already processing'
            job.delete()
            return False#Do not need to put the item back to the tube
        t = ReSendThread(input_tube, output_tube, timeout)
        self.add_work_thread(input_tube, t)
        t.start()
        job.delete()
        return False#Do not need to put the item back to the tube

    
    
        
if __name__ == "__main__":
    s = SimpleService({
                            "input": "Input tube for generator",
                            "output": "Output tube for generator",
                      },
                      ReSendService)
    s.run()