import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread, beanstalkServiceApp
from libs.services.servicebase import service
from django.conf import settings
from ui_framework.objsys.models import UfsObj
from tagging.models import Tag, TaggedItem
import threading
import traceback
from ui_framework.connection.models import Processor
import json
import time
import datetime
from django.utils.timezone import utc
import uuid
import os
from libs.logsys.logSys import *
import libs.utils.objTools as objtools
from libs.services.svc_base.simpleservice import SimpleService
from libs.services.svc_base.state import StatefulProcessor
from libs.utils.misc import ensureDir as ensure_dir
from django.utils.timezone import utc


gTagExporterProcessorId = '262b85e8-ccd3-41ae-854d-7518c1c803f6'


class TagExporter(beanstalkServiceApp, StatefulProcessor):
    def startServer(self):
        root_dir = libsys.get_root_dir()

        param = self.get_state(gTagExporterProcessorId, {"timestamp": 0})
        
        result_dict = {}
        
        if True:
            last_timestamp = param["timestamp"]
            print last_timestamp
            
            #print last_timestamp
            if 0 == last_timestamp:
                print 'timestamp is zero'
                tagged_item_list = TaggedItem.objects.order_by('timestamp')
            else:
                django_time = datetime.datetime.fromtimestamp(last_timestamp).replace(tzinfo=utc)
                print django_time
                tagged_item_list = TaggedItem.objects.filter(timestamp__gt=django_time).order_by('timestamp')
                
            for tagged_item in tagged_item_list:
                if "system:auto-app" in tagged_item.tag.name:
                    #Ignore system auto app tag
                    continue
                obj_tag = tagged_item.tag.name
                obj = tagged_item.object
                tag_app = tagged_item.tag_app

                print obj, tagged_item.timestamp, last_timestamp
                if result_dict.has_key(obj.ufs_url):
                    result_dict[obj.ufs_url]["tags"].append({"tag": obj_tag, "app": tag_app})
                else:
                    result_dict[obj.ufs_url] = {"tags": [{"tag": obj_tag, "app": tag_app}], "uuid": obj.uuid}
                last_timestamp = time.mktime(tagged_item.timestamp.timetuple())
                if self.quit_flag:
                    break
                time.sleep(1)

        
        ######
        # Quitting, so save last_timestamp
        final_data = []
        for ufs_url in result_dict:
            final_data.append({"tags": result_dict[ufs_url]["tags"], "ufs_url": ufs_url, "uuid": result_dict[ufs_url]["uuid"]})

        
                
        ######
        # Quitting, so save last_timestamp
        if 0 != len(final_data):
            
            dump_root = os.path.join(root_dir, "../tag_dump/")
            ensure_dir(dump_root)
            
            dump_filename = os.path.join(root_dir, "../tag_dump/"+str(time.time())+".json")
            f = open(dump_filename, "w")
            f.write(json.dumps(final_data, indent=4))
            f.close()
            
            param["timestamp"] = last_timestamp
            self.set_state(gTagExporterProcessorId, param)
            
        else:
            print "No more tag applied"
                


        
if __name__ == "__main__":
    s = SimpleService({
                            "input": "Input tube for generator",
                            "output": "Output tube for generator",
                      },
                      TagExporter)
    s.run()