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

gTubeLoggingServiceName = 'tube_logging_service_tube'

class DjangoCollection:
    def get(self, name_in_coll):
        pass
    def set(self, name_in_coll, obj_url):
        pass

class StorageWithDomainThread(SimpleWorkThread):
    def thread_init(self):
        #Load domain info

    def processItem(self, job, item):

        #job.delete()
        #return False#Do not need to put the item back to the tube



if __name__ == "__main__":
    s = SimpleService({
                            "input": "input tube name",
                            "output_path": "output path for the stoarge",
                            #"blacklist": "blacklist for scanning, example: *.exe",
                        },
                        thread_class = StorageWithDomainThread)
    s.run()