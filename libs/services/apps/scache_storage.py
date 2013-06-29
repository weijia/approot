import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread, beanstalkServiceApp
#from libs.services.servicebase import service
#from django.conf import settings
from ui_framework.objsys.models import UfsObj
#from tagging.models import Tag, TaggedItem
#import threading
#import traceback
from libs.windows.changeNotifyThread import changeNotifyThread
import libs.utils.transform as transform
import os
import time
import json
import beanstalkc
#from configuration import g_config_dict

#gMonitorServiceTubeName = "monitorQueue"
#gFileListTubeName = "fileList"
#gMaxMonitoringItems = 100
from libs.services.svc_base.simpleservice import SimpleService

            
class ScacheStorageServiceApp(beanstalkServiceApp):
    def processItem(self, job, item):
        url = item["url"]
        cached_path = item["cached_path"]
        cached_path = transform.transformDirToInternal(cached_path)
        o = UfsObj.objects.filter(ufs_url = url)
        if 0 == o.count():
            s = UfsObj(ufs_url = url, full_path = cached_path)
            s.save()
        else:
            found = False
            for i in o:
                if i.full_path == cached_path:
                    #Already saved, ignore this storage
                    found = True
                    break
            if not found:
                s = UfsObj(ufs_url = url, full_path = cached_path)
                s.save()
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True

    
        
if __name__ == "__main__":
    s = SimpleService({
                            "input":"Input tube for path to monitor", 
                            "output":"Output tube for changed files"
                      },
                      ScacheStorageServiceApp)
    s.run()