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
from libs.services.svc_base.simpleservice import SimpleService
from libs.utils.misc import ensureDir as ensure_dir

gTubeLoggingServiceName = 'tube_logging_service_tube'

class LoggingThread(beanstalkWorkingThread):
    def __init__(self, input_tube, output_tube):
        super(LoggingThread, self).__init__(input_tube)
        self.input_tube = input_tube
        self.output_tube = output_tube
        
        root_dir = libsys.get_root_dir()
        dump_root = os.path.join(root_dir, "../tube_log/")
        ensure_dir(dump_root)
        self.output_file = open(os.path.join(dump_root, 'tube_output.txt'), "w")
        print 'tube log created'
    def processItem(self, job, item):
        print 'item received in tube log:', item
        s = json.dumps(item, sort_keys=True, indent=4)
        print >>self.output_file, s
        if self.output_tube is None:
            #Do not put the item to target tube
            job.delete()
            return False#Do not need to put the item back to the tube
        self.put_item(item, self.output_tube)
        job.delete()
        
        return False#Do not need to put the item back to the tube



class LoggingService(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, tube_name = gTubeLoggingServiceName):
        '''
        Constructor
        '''
        super(LoggingService, self).__init__(tube_name)


    def processItem(self, job, item):
        input_tube = item["input"]
        output_tube = item.get("output", None)

        if self.is_processing_tube(input_tube):
            print 'input tube already processing'
            job.delete()
            return False#Do not need to put the item back to the tube
        t = LoggingThread(input_tube, output_tube)
        self.add_work_thread(input_tube, t)
        t.start()
        job.delete()
        return False#Do not need to put the item back to the tube

 
        
if __name__ == "__main__":
    s = SimpleService({
                            "input": "input tube name",
                            "output": "output tube name, optional",
                            #"blacklist": "blacklist for scanning, example: *.exe",
                        },
                        LoggingService)
    s.run()