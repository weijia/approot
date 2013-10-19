'''
Created on 2012-02-13

@author: Richard
'''
import os
import time
import beanstalkc
import traceback
import threading
import sys
#import uuid
import libsys
import time
#from localLibs.windows.changeNotifyThread import changeNotifyThread
import json
#import localLibs.server.XmlRpcServer2BeanstalkdServiceBridge as bridge
from configuration import g_config_dict
gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = g_config_dict["ufs_beanstalkd_port"]
#gMonitorServiceinput_input_tube_name = "monitorQueue"
gItemDelayTime = 60*60*24#One day
g_stop_msg_priority = 0
gBeanstalkdLauncherServiceTubeName = "beanstalkd_launcher_service"
import time

class beanstalkServiceBase(object):
    '''
    basic communication with msg service
    '''
    def __init__(self, input_tube_name = None):
        '''
        Constructor
        '''
        if input_tube_name is None:
            input_tube_name = self.__class__.__name__ + "_default_cmd_input_tube_name"
        self.input_tube_name = input_tube_name
        self.quit_signal_channel_name = input_tube_name + "_stop_tube"
        #print 'port: ', gBeanstalkdServerPort
        self.beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        self.default_timestamp = time.time()

    def get_input_tube_name(self):
        return self.input_tube_name
        
    def put_item(self, item_dict, target_tube, priority = beanstalkc.DEFAULT_PRIORITY, delay = 0):
        #print 'port: ', gBeanstalkdServerPort
        beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        try:
            beanstalk.use(target_tube)
        except:
            print 'using: "%s"',target_tube
        s = json.dumps(item_dict, sort_keys=True, indent=4)
        if hasattr(self, 'input_tube_name'):
            print "add item: %s, from: %s, to: %s, priority: %d"%(s, self.input_tube_name, target_tube, priority)
        else:
            print "add item: %s, to: %s, priority: %d"%(s, target_tube, priority)
        job = beanstalk.put(s, priority = priority, delay = delay)
        return job
    
    def addItem(self, itemDict, priority = beanstalkc.DEFAULT_PRIORITY):
        return self.put_item(itemDict, self.input_tube_name, priority)
        
    def put(self, itemDict, priority = beanstalkc.DEFAULT_PRIORITY, delay = 0):
        return self.put_item(itemDict, self.input_tube_name, priority, delay=delay)

    def watch_service_and_private_tube(self):
        print 'watch tube: ', self.input_tube_name
        self.beanstalk.ignore('default')
        self.beanstalk.watch(self.quit_signal_channel_name)
        while True:
            stop_msg = self.beanstalk.reserve(0)
            if stop_msg is None:
                break
            else:
                stop_msg.delete()
            print "ignore existing stop msg"
        self.beanstalk.watch(self.input_tube_name)
        
        
    def is_term_signal(self, item):
        if isinstance(item, dict) and item.has_key("cmd"):
            if item["cmd"] == "stop":
                print "got a quit message"
                return True
        return False
    
    def processItem(self, job, item):
        print 'calling default processItem'
        if item.has_key("default_session_timestamp"):
            if self.default_timestamp == item["default_session_timestamp"]:
                try:
                    self.procCurSessionItem(job, item)
                except:
                    traceback.print_exc()
            else:
                try:
                    self.procPrevSessionItem(job, item)
                except:
                    traceback.print_exc()
        job.delete()
        return False#Return False if we do not need to put the item back to tube
    
    def stop(self):
        print "got a quit message"



class beanstalkServiceApp(beanstalkServiceBase):
    def __init__(self, input_tube_name = None):
        super(beanstalkServiceApp, self).__init__(input_tube_name)
        ##############################
        # The thread should be value not the key, input tube should be the key
        ##############################
        self.input_channel_name_to_work_thread_dict = {}
        self.quit_flag = False
        
    def watch_private_tube(self):
        print 'watch tube: ', self.input_tube_name
        self.beanstalk.ignore('default')
        self.beanstalk.watch(self.quit_signal_channel_name)
        while True:
            stop_msg = self.beanstalk.reserve(0)
            if stop_msg is None:
                break
            else:
                stop_msg.delete()
            print "ignore existing stop msg"
            
    def load_msg_without_exception(self, timeout = None):
        try:
            if timeout is None:
                job = self.beanstalk.reserve()
            else:
                job = self.beanstalk.reserve(timeout=timeout)
                print 'msg receive timeout'
        except:
            print 'receive exception, return from load_msg_without_exception'
            #self.stop()
            traceback.print_exc()
            raise
            #return None, None
        if job is None:
            return None, None
        print "got job", job.body
        try:
            item = json.loads(job.body)
        except:
            print 'Decode JSON string error', job.body
            traceback.print_exc()
            job.delete()
            return None, None
        return job, item
        
    def register_service_tube(self):
        '''
        Watch private tube. Do not clean private tube at this time, otherwise, useful message such as registration will be cleaned.
        return True, if registere OK
        return False, if register fail, should quit service app
        '''
        print 'watch tube: ', self.input_tube_name
        self.beanstalk.ignore('default')
        self.beanstalk.watch(self.quit_signal_channel_name)
        
        self.pid = os.getpid()
        print "current pid: ", self.pid
        
        is_register_ok = False
        put_delay = 2#Seconds
        wait = False
        cnt = 0
        ########################
        #First register, after register, clean will be done by master service app, so no useful msg will be cleaned by accident
        ########################
        while True:
            wait = False
            self.put_item({
                            "cmd": "registration", "pid": self.pid, "service_input_tube_name": self.input_tube_name,
                            "private_input_tube_name": self.quit_signal_channel_name, "timestamp": time.time()
                       }, 
                       gBeanstalkdLauncherServiceTubeName)
            if cnt > 100:
                ##################
                # Avoid dead loop
                ##################
                return False
            job, item = self.load_msg_without_exception(10)#time out is in seconds
            
            if job is None:
                print 'receive msg error, retry...', self.get_input_tube_name()
                ###################
                # Receive failed, quiting
                continue
            
            if item.has_key('timestamp') and (item["timestamp"] + 20 < time.time()):
                ###################
                #Very old control msg, ignore it
                print 'duplicated service register signal received final return from msg receiving loop'
                job.delete()
                continue
            if not item.has_key('timestamp'):
                print 'no timestamp'
                job.delete()
                continue
                
            if item.has_key("cmd") and (item["cmd"] == "tube_already_registered"):
                if self.pid == item["pid"]:
                    print "duplicated service register"
                    #self.stop()
                    print 'duplicated service register signal received final return from msg receiving loop'
                    job.delete()
                    ###################
                    # Receive failed, quiting
                    return False
                
            if item.has_key("cmd") and (item["cmd"] == "register_ok"):
                if self.pid == item["pid"]:
                    is_register_ok = True
                    print 'register OK'
                    job.delete()
                    #It is the master service app, shall be responsible for clean stop msg is there is some
                    break
                
                else:
                    #If received brother registration signal, put it without delay and
                    put_delay = 0
                    wait = True
                    print "find brother", self.pid, item["pid"]
            #Put the msg back as we are not the target for this command

            #This is not a register msg, put it back
            job.release(priority = beanstalkc.DEFAULT_PRIORITY, delay = put_delay)
            print "msg sent back, back to msg loop"
            if wait:
                time.sleep(1)
        ######################
        #End of registration loop
        ######################
            
        if is_register_ok:
            #Clean stop msgs
            while True:
                stop_msg = self.beanstalk.reserve(0)
                if stop_msg is None:
                    break
                else:
                    stop_msg.delete()
                print "ignore existing stop msg"
            ##################
            #Start service
            ##################
            self.beanstalk.watch(self.input_tube_name)
        else:
            #Unknown error
            print "unknown error"
        return True
        
    def add_work_thread(self, work_thread_input_tube, thread_instance):
        self.input_channel_name_to_work_thread_dict[work_thread_input_tube] = thread_instance
        
    def is_processing_tube(self, work_thread_input_tube):
        return self.input_channel_name_to_work_thread_dict.has_key(work_thread_input_tube)
    
    def msg_loop(self):
        while True:
            job, item = self.load_msg_without_exception()
            if job is None:
                print 'receive error, returning'
                return
            if self.is_term_signal(item):
                self.stop()
                print 'stop signal received final return from msg receiving loop'
                job.delete()
                return
                #continue
                
            print item
            try:
                if self.processItem(job, item):
                    #If return True, the job was processed but should be still in queue, release and delay it
                    job.release(priority = beanstalkc.DEFAULT_PRIORITY, delay = gItemDelayTime)
                ########################################
                # !!! Otherwise, sub class must delete the item. Or timeout will occur
                ########################################
            except Exception,e:
                print >>sys.stderr, "processing task error, ignore the following"
                traceback.print_exc()
                #raise e
                job.delete()
    
    def startServer(self):
        #!!!Not working: Kick all items to active when start, as we bury them in the previous processing
        #kickedItemNum = beanstalk.kick(gMaxMonitoringItems)
        #print kickedItemNum
        if not self.register_service_tube():
            print('register failed, returning')
            return
        self.msg_loop()
                
    def stop(self):
        '''
        This function will only be called after registration is OK
        '''
        #Set this flag here as well.
        self.quit_flag = True
        #Tell all sub process to stop
        for input_channel_name in self.input_channel_name_to_work_thread_dict:
            ########################
            # Stop msg should not be delayed so master service app can clean it after registration. Otherwise, some stop msg will be got after the cleanning is done
            self.put_item({"cmd": "stop"}, 
                          self.input_channel_name_to_work_thread_dict[input_channel_name].quit_signal_channel_name,
                          g_stop_msg_priority)
            self.input_channel_name_to_work_thread_dict[input_channel_name].external_stop()
            print "working thread stop msg sent"
            
    #############################
    # The following function will be called from outside of this.
    # So it must be thread safe
    #############################
    def external_stop(self):
        self.quit_flag = True


class beanstalkWorkingThread(beanstalkServiceApp, threading.Thread):
    def __init__ ( self, inputinput_tube_name):
        beanstalkServiceApp.__init__(self, inputinput_tube_name)
        threading.Thread.__init__(self)
        
    def run(self):
        self.startServer()
        
    def stop(self):
        self.quit_flag = True

        
if __name__ == "__main__":
    s = beanstalkServiceBase()
    s.startServer()