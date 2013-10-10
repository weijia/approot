import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread, beanstalkServiceApp

from libs.windows.changeNotifyThread import changeNotifyThread
import libs.utils.transform as transform
import os
import time
import json
import beanstalkc
gBeanstalkdServerHost = '127.0.0.1'

from libs.services.svc_base.simpleservice import SimpleService

#gBeanstalkdServerPort = 11300

#gMonitorServiceTubeName = "monitorQueue"
#gFileListTubeName = "fileList"
#gMaxMonitoringItems = 100


class changeNotifyForBeanstalkd(changeNotifyThread):
    def __init__(self, fullPath, targetTube, blackList = []):
        super(changeNotifyForBeanstalkd, self).__init__(fullPath)
        self.blackList = blackList
        self.targetTube = targetTube
    def callback(self, pathToWatch, relativePath, changeType):
        fullPath = transform.format_path(os.path.join(pathToWatch, relativePath))
        itemDict = {"monitoringPath": transform.format_path(pathToWatch),
                        "fullPath": fullPath, "changeType":changeType,
                        "timestamp": time.time()}
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalk.use(self.targetTube)
        #print beanstalk.using()
        s = json.dumps(itemDict, sort_keys=True, indent=4)
        job = beanstalk.put(s)

class MonitorThread(beanstalkWorkingThread):
    def __init__ ( self, input_tube, output_tube_name):
        super(MonitorThread, self).__init__(input_tube)
        self.input_tube = input_tube
        self.output_tube_name = output_tube_name
        self.notifyThreads = {}
        
    def processItem(self, job, item):
        fullpath = transform.format_path(item["fullpath"])
        if not os.path.exists(fullpath) or self.notifyThreads.has_key(fullpath):
            print 'Path: %s already in monitoring'%fullpath
            job.delete()
            return False
        if not os.path.isdir(fullpath):
            cl("file change is not supported yet:", fullpath)
            job.delete()
            return False
        t = changeNotifyForBeanstalkd(fullpath, self.output_tube_name)
        self.notifyThreads[fullpath] = t
        t.start()
        return True
    def stop(self):
        #Set this flag here as well.
        self.quit_flag = True
        #Tell all sub process to stop
        for full_path in self.notifyThreads:
            self.notifyThreads[full_path].exit()
        print 'stop monitoring set'
            
class MonitorServiceApp(beanstalkServiceApp):
    def processItem(self, job, item):
        input_tube = item["input"]
        output_tube = item["output"]
        t = MonitorThread(input_tube, output_tube)
        if self.is_processing_tube(input_tube+":"+output_tube):
            job.delete()
            return False
        self.add_work_thread(input_tube+":"+output_tube, t)
        print 'Starting new working thread'
        t.start()
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True


    
    
    
    
        
if __name__ == "__main__":
    s = SimpleService({"input":"Input tube for path to monitor", "output":"Output tube for changed files"}, MonitorServiceApp)
    s.run()