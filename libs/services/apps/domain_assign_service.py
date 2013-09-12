'''
Created on 2012-05-18

@author: Richard
'''
import os
import time
#import beanstalkc
import libsys
#from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread, beanstalkServiceApp
import libs.utils.simplejson as json
from libs.services.svc_base.simpleservice import SimpleService, SimpleWorkThread
from django.conf import settings
from objsys.models import UfsObj


class DomainAssignThread(SimpleWorkThread):
    def add_task_info(self, item):
        super(DomainAssignThread, self).add_task_info(item)
        self.domain_name = item["domain"]
        self.domain_tags = item["tags"].split(",")
        

    def processItem(self, job, item):
        objlist = UfsObj.objects.filter(full_path=item["full_path"])
        if 0 != objlist:
            for obj in objlist:
                if obj.tags in self.domain_tags:
                    item["domain"] = self.domain_name
                    break
        self.output(item)
        job.delete()
        return False#Do not need to put the item back to the tube



if __name__ == "__main__":
    s = SimpleService({
                            "input": "input tube name",
                            "output": "output tube name, optional",
                            "tags": "tag list for the domain",
                            "domain": "domain name to put for all object with above tags (any one of the tags)"
                            #"blacklist": "blacklist for scanning, example: *.exe",
                        },
                        thread_class = DomainAssignThread)
    s.run()