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
from tag_importer import StatefulProcessor
from libs.utils.misc import ensureDir as ensure_dir
import libs.utils.transform as transform

gTagExporterProcessorId = '27cafbf5-8d5d-4ec1-9ca5-b7de85dfce2a'


def add_tag_for_full_path(full_path, tag, tag_app = None):
    full_path = transform.transformDirToInternal(full_path)
    obj_list = UfsObj.objects.filter(full_path = full_path)
    if 0 == obj_list.count():
        ufs_url = objtools.getUfsUrlForPath(full_path)
        obj = UfsObj(ufs_url = ufs_url, full_path=full_path)
        obj.save()
    else:
        obj = obj_list[0]
    Tag.objects.add_tag(obj, tag, tag_app)


class FolderTagging(beanstalkServiceApp, StatefulProcessor):
    def startServer(self):
        root_dir = libsys.get_root_dir()

        param = self.get_state(gTagExporterProcessorId, {"timestamp": 0})
        
        #result_dict = {}
        
        if True:
            last_timestamp = param["timestamp"]
            print last_timestamp
            
            #print last_timestamp
            if 0 == last_timestamp:
                print 'timestamp is zero'
                tagged_item_list = TaggedItem.objects.order_by('timestamp')
            else:
                django_time = datetime.datetime.fromtimestamp(last_timestamp)
                print django_time
                tagged_item_list = TaggedItem.objects.filter(timestamp__gt=django_time).order_by('timestamp')
                
            for tagged_item in tagged_item_list:
                if "system:auto-app" == tagged_item.tag.name:
                    #Ignore system auto app tag
                    continue
                if "git" == tagged_item.tag.name:
                    #Ignore system auto app tag
                    continue
                if "svn" == tagged_item.tag.name:
                    #Ignore system auto app tag
                    continue
                obj_tag = tagged_item.tag.name
                obj = tagged_item.object
                tag_app = tagged_item.tag_app

                print obj, tagged_item.timestamp, last_timestamp
                '''
                if result_dict.has_key(obj.ufs_url):
                    result_dict[obj.ufs_url]["tags"].append({"tag": obj_tag, "app": tag_app})
                else:
                    result_dict[obj.ufs_url] = {"tags": [{"tag": obj_tag, "app": tag_app}], "uuid": obj.uuid}
                '''
                if os.path.isdir(obj.full_path):
                    for folder_path, folders, filenames in os.walk(obj.full_path):
                        for filename in filenames:
                            target_full_path = os.path.join(folder_path, filename)
                            add_tag_for_full_path(target_full_path, obj_tag, 'app:folder_tagging')
                            if self.quit_flag:
                                break
                        for ignore_folder in ['.git', '.svn']:
                            if ignore_folder in folders:
                                folders.remove(ignore_folder)
                        for folder in folders:
                            target_full_path = os.path.join(folder_path, folder)
                            add_tag_for_full_path(target_full_path, obj_tag, 'app:folder_tagging')
                            if self.quit_flag:
                                break
                        if self.quit_flag:
                            break
                if self.quit_flag:
                    break                        
                last_timestamp = time.mktime(tagged_item.timestamp.timetuple())
            time.sleep(1)

        
        ######
        # Quitting, so save last_timestamp
        param["timestamp"] = last_timestamp
        self.set_state(gTagExporterProcessorId, param)
                


        
if __name__ == "__main__":
    s = SimpleService({
                            "input": "Input tube for generator",
                            "output": "Output tube for generator",
                      },
                      FolderTagging)
    s.run()