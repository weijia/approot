# -*- coding: gbk -*-
import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread, beanstalkServiceApp
from libs.services.servicebase import service
from django.conf import settings
from ui_framework.objsys.models import UfsObj
from tagging.models import Tag, TaggedItem
import threading
import traceback
#from ui_framework.connection.models import Processor
import json
import time
import datetime
from django.utils.timezone import utc
#import uuid
#import os
from libs.logsys.logSys import *
from libs.services.svc_base.simpleservice import SimpleService
from libs.services.svc_base.state import StatefulProcessor

gTagExporterProcessorId = '262b85e8-ccd3-41ae-854d-7518c1c803f6'


            
class AllTagEnumThread(beanstalkWorkingThread, StatefulProcessor):
    def __init__(self, input, output, diagram_id, session_id):
        '''
        Constructor
        '''
        #self.beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
        beanstalkServiceApp.__init__(self, input)
        threading.Thread.__init__(self)
        self.output = output
        #self.first_tag_timestamp = first_tag_timestamp
        self.session_id = session_id
        self.diagram_id = diagram_id
        self.quit_flag = False
        self.last_timestamp = 0
    '''            
    def restart(self):
        if self.last_timestamp + 10 > time.time():
            #Only restart when timestamp is not updated for 10 seconds
            pass
    
    #We can not use the following codes as if an item is just processed, then the processor will not send a restart msg.
    def is_processing(self):
        if self.last_timestamp + 10 > time.time():
            #Only restart when timestamp is not updated for 10 seconds
            return False
        else:
            return True
    '''
    def get_last_processing_timestamp(self):
        return self.last_timestamp
        
    def run(self):
        print 'watch tube: ', self.input_tube_name
        self.beanstalk.ignore('default')
        self.beanstalk.watch(self.input_tube_name)

        #Send a msg to self to trigger the first processing loop
        self.put({"start": True})
        #Start the msg loop
        self.msg_loop()
        
    def processItem(self, job, item):
        job.delete()
        param = self.get_state(self.diagram_id, {'all_tag_enum_start_timestamp': 0})
        first_tag_timestamp = param["all_tag_enum_start_timestamp"]
        print first_tag_timestamp
        if item.has_key("timestamp"):
            self.last_timestamp = item["timestamp"]
        if 0 == first_tag_timestamp:
            ncl('timestamp is zero')
            tagged_item_list = TaggedItem.objects.order_by('timestamp')
        else:
            django_time = datetime.datetime.fromtimestamp(first_tag_timestamp).replace(tzinfo=utc)
            cl("timestamp", django_time, first_tag_timestamp)
            tagged_item_list = TaggedItem.objects.filter(timestamp__gt=django_time).order_by('timestamp')
        for tagged_item in tagged_item_list:
            if "system:auto-app" in tagged_item.tag.name:
                #Ignore system auto app tag
                continue
            obj_tag = tagged_item.tag.name
            obj = tagged_item.object
            tag_app = tagged_item.tag_app

            cl(obj, tagged_item.timestamp, first_tag_timestamp, time.mktime(tagged_item.timestamp.timetuple()) + (tagged_item.timestamp.microsecond/1000000.0))
            
            self.put_item({"session_id": self.session_id, "ufs_url": obj.ufs_url, 
                            "uuid": obj.uuid, "full_path": obj.full_path, "tag": obj_tag, "tag_app": tag_app, 
                                "timestamp": time.mktime(tagged_item.timestamp.timetuple()) + 
                                            (tagged_item.timestamp.microsecond/1000000.0), 
                                "diagram_id": self.diagram_id}, 
                            self.output)
            if self.quit_flag:
                break
            time.sleep(1)
        return False
    '''        
    def add_tagged(self, item):
        item["session_id"] = self.session_id
        item["diagram_id"] = self.diagram_id
        self.put_item(item, self.output)
    '''

    
class AllTagEnumeratorService(beanstalkServiceApp):
    def __init__(self):
        super(AllTagEnumeratorService, self).__init__("all_tag_enumerator_service_global_input")
        self.cnt = 0
        self.last_msg_timestamp = {}
    def processItem(self, job, item):
        if item.has_key("dynamic_tag"):
            timestamp = time.time()
            for diagram_id in self.input_channel_name_to_work_thread_dict:
                thread_last_timestamp = self.input_channel_name_to_work_thread_dict[diagram_id].get_last_processing_timestamp()
                if thread_last_timestamp >= self.last_msg_timestamp[diagram_id]:
                    #相等的话表示最后一个发给thraed的消息已经被处理掉，如果大于呢？应该是不可能有大于
                    self.input_channel_name_to_work_thread_dict[diagram_id].put({"restart": True, "timestamp": timestamp})
        else:        
            output_tube = item["output"]
            #timestamp will be retrieved from process state.
            #timestamp = item["timestamp"]
            diagram_id = item["diagram_id"]
            session_id = item.get("session_id", 0)

            t = AllTagEnumThread('all_tag_enumerator_service_work_thread_tube_%d'%self.cnt, output_tube, diagram_id, session_id)
            self.add_work_thread(diagram_id, t)
            self.last_msg_timestamp[diagram_id] = 0
            t.start()
        job.delete()
        return False#Do not need to put the item back to the tube


        
if __name__ == "__main__":
    s = SimpleService({
                            "output": "Output tube for generator",
                            #"session_id": "Used to identify this session, so previous session msg will be ignored", #now default in simple processor
                            #"diagram_id": "Each process diagram has an ID, it is used to save diagram related parameters", #now default in simple processor
                      },
                      AllTagEnumeratorService)
    s.run()