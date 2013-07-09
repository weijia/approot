# -*- coding: gbk -*-
from django.utils.timezone import utc
import datetime
import libsys
from libs.logsys.logSys import *
from django.conf import settings
from libs.services.svc_base.managed_service import WorkerBase
from libs.tagging.models import TaggedItem


class AllTagEnum(WorkerBase):
    '''
    没有Service结尾的作为worker thread
    '''
        
    def process(self, msg):
        #Retrieve saved last timestamp, will start to enumerate items with greater (not equal) timestamp
        first_tag_timestamp = self.state.get_state_value("all_tag_enum_start_timestamp", 0)
        cl(first_tag_timestamp)
        
        tagged_item_list = self.get_tagged_items_greater_than_timestamp(first_tag_timestamp)
        
        #Send all retieved items
        for tagged_item in tagged_item_list:
            if "system:auto-app" in tagged_item.tag.name:
                #Ignore system auto app tag
                continue
            obj_tag = tagged_item.tag.name
            obj = tagged_item.object
            tag_app = tagged_item.tag_app

            cl(obj, tagged_item.timestamp, first_tag_timestamp, time.mktime(tagged_item.timestamp.timetuple()) + 
                    (tagged_item.timestamp.microsecond/1000000.0))
            
            self.output.send({"session_id": self.session_id, "ufs_url": obj.ufs_url, 
                            "uuid": obj.uuid, "full_path": obj.full_path, "tag": obj_tag, "tag_app": tag_app, 
                                "timestamp": time.mktime(tagged_item.timestamp.timetuple()) + 
                                            (tagged_item.timestamp.microsecond/1000000.0), 
                                "diagram_id": self.diagram_id})

            if self.is_quitting():
                break
            time.sleep(1)
        msg.set_processed()

    def get_tagged_items_greater_than_timestamp(self, first_tag_timestamp):
        if 0 == first_tag_timestamp:
            ncl('timestamp is zero')
            tagged_item_list = TaggedItem.objects.order_by('timestamp')
        else:
            django_time = datetime.datetime.fromtimestamp(first_tag_timestamp).replace(tzinfo=utc)
            cl("timestamp", django_time, first_tag_timestamp)
            tagged_item_list = TaggedItem.objects.filter(timestamp__gt=django_time).order_by('timestamp')
            
            
from libs.services.svc_base.simple_service_v2 import SimpleService

if __name__ == "__main__":
    s = SimpleService({
                            "output": "Output msg queue for this generator",
                      },
                      worker_thread_class = AllTagEnum)
    #s.run()
