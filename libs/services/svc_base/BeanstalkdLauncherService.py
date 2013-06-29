'''
Created on 2012-02-13

@author: Richard
'''
#import os
import time
import beanstalkc
#import traceback
#import threading

import libsys
import libs.utils.simplejson as json
#Use full package path as the app will be executed in any where in the tree
from libs.services.svc_base.beanstalkd_interface import beanstalkServiceApp
from libs.services.svc_base.beanstalkd_interface import gBeanstalkdLauncherServiceTubeName, g_stop_msg_priority
from libs.logsys.logSys import *

        
class BeanstalkdLauncherService(beanstalkServiceApp):
    def __init__(self, tube_name = gBeanstalkdLauncherServiceTubeName):
        super(BeanstalkdLauncherService, self).__init__(tube_name)
        self.taskid_service_tube_dict = {}
        self.taskid_private_tube_name_dict = {}
        self.service_tube_name2pid = {}
        
    def watchTube(self):
        print 'watch tube: ', self.get_input_tube_name()
        self.beanstalk.ignore('default')
        self.beanstalk.watch(self.quit_signal_channel_name)
        self.beanstalk.watch(self.get_input_tube_name())
        print 'watching:', self.quit_signal_channel_name, self.get_input_tube_name()
        while True:
            stop_msg = self.beanstalk.reserve(0)
            if stop_msg is None:
                break
            else:
                stop_msg.delete()
            print "ignore existing msg:", stop_msg.body
        print '------------------------------------------------Launcher service started OK'

    def startServer(self):
        self.watchTube()
        #!!!Not working. Kick all items to active when start, as we bury them in the previous processing
        #kickedItemNum = beanstalk.kick(gMaxMonitoringItems)
        #print kickedItemNum
        '''
        taskid_private_tube_name_dict: pid->stop_tube_name
        taskid_service_tube_dict: pid->service_tube_name
        service_tube_name2pid: service_tube_name->pid
        '''
        while True:
            try:
                job = self.beanstalk.reserve()
            except:
                self.stop()
                return
            print "got job", job.body
            item = json.loads(job.body)
            #For compatitible for legacy beanstalkd service
            if item.has_key("service_input_tube_name"):
                item["service_tube_name"] = item["service_input_tube_name"]
            if item.has_key("private_input_tube_name"):
                item["private_tube_name"] = item["private_input_tube_name"]
                
            if item.has_key("cmd"):
                if item["cmd"] == "registration":
                    if item.has_key("pid") and item.has_key("service_tube_name"):
                        if self.service_tube_name2pid.has_key(item["service_tube_name"]):
                            #Service tube name already registered, stop it
                            if self.taskid_service_tube_dict.has_key(item["pid"]) and (self.taskid_service_tube_dict[item["pid"]] == item["service_tube_name"]):
                                print "already registered, same service tube name, ignore it"
                            else:
                                print "registered but not the same, send notification"
                                self.put_item({"cmd":"tube_already_registered", "pid": item["pid"], "timestamp": time.time()}, item["private_tube_name"])
                        else:
                            #No service on this service tube name registered
                            self.taskid_service_tube_dict[item["pid"]] = item["service_tube_name"]
                            self.taskid_private_tube_name_dict[item["pid"]] = item["private_tube_name"]
                            self.service_tube_name2pid[item["service_tube_name"]] = item["pid"]
                            self.put_item({"cmd":"register_ok", "pid": item["pid"], "timestamp": time.time()}, item["private_tube_name"])
                    else:
                        print "invalid pid or service_tube_name, item:", item
                elif item["cmd"] == "stop":
                    if item.has_key("pid"):
                        if self.taskid_private_tube_name_dict.has_key(item["pid"]):
                            self.put_item({"cmd":"stop", "sender": "BeanstalkdLauncherService-stop-msg-received"}, self.taskid_private_tube_name_dict[item["pid"]])
                        else:
                            print "no tube name registered for pid", item["pid"], self.taskid_private_tube_name_dict
                    else:
                        print "not a valid cmd", item
            
            job.delete()
    '''
    #This function is not used should be removed later.
    def send_stop_signals(self):
        for i in self.taskid_cmd_tube_name_dict:
            self.put_item({"cmd":"stop"}, self.taskid_cmd_tube_name_dict[i], g_stop_msg_priority)
    '''
    def send_stop_for_pid(self, pid):
        try:
            self.addItem({"cmd":"stop", "pid": pid, "sender": "BeanstalkdLauncherService-send_stop_for_pid"}, g_stop_msg_priority)
            cl("Send stop signals")
        except beanstalkc.SocketError:
            cl("beanstalkd seems terminated")

if __name__ == "__main__":
    s = BeanstalkdLauncherService(gBeanstalkdLauncherServiceTubeName)
    s.startServer()