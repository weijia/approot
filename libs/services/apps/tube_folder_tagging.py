from libs.services.svc_base.managed_service import WorkerBase
import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread, beanstalkServiceApp
#from libs.services.servicebase import service
from django.conf import settings
from ui_framework.objsys.models import UfsObj
from libs.tagging.models import Tag, TaggedItem
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
import libs.utils.obj_tools as obj_tools
#from libs.services.svc_base.simpleservice import SimpleService, SimpleWorkThread
from libs.services.svc_base.state import StatefulProcessor
from libs.utils.misc import ensureDir as ensure_dir
import libs.utils.transform as transform


def add_tag_for_full_path(full_path, tag, tag_app = None):
    full_path = transform.transformDirToInternal(full_path)
    obj_list = UfsObj.objects.filter(full_path = full_path)
    if 0 == obj_list.count():
        ufs_url = obj_tools.getUfsUrlForPath(full_path)
        obj = UfsObj(ufs_url = ufs_url, full_path=full_path)
        obj.save()
    else:
        obj = obj_list[0]
    Tag.objects.add_tag(obj, tag, tag_app)
    
    #Add folder tag
    if os.path.isdir(full_path):
        Tag.objects.add_tag(obj, "system:folder", tag_app)
    else:
        #Add media tags
        obj_type = obj.get_type()
        cl(full_path, obj_type)
        if 'image' in obj_type:
            Tag.objects.add_tag(obj, "system:pic", tag_app)
        else:
            isVideo = False
            for signature in ['RIFF (little-endian) data, AVI', 'RealMedia file', 
                                'Matroska data', 'Macromedia Flash Video']:
                if signature in obj_type:
                    Tag.objects.add_tag(obj, "system:video", tag_app)
                    break
            
            
            
gDefaultAutoTagIgnoreTagsList = ["git", "svn"]
gDefaultAutoTagIgnoreFolderList = [".git", '.svn',]
gDefaultAutoTagIgnoreFileList = ['autorun.inf', 'Thumbs.db', ]
gAutoTagServiceAppName = 'app:folder_tagging'
    
class FolderTaggingThread(WorkerBase, StatefulProcessor):
    def thread_init(self):
        self.last_timestamp = 0
    def processItem(self, job, item):
        '''
            self.put_item({"session_id": self.session_id, "ufs_url": obj.ufs_url, "uuid": obj.uuid, "full_path": obj.full_path, 
                            "tag": obj_tag, "tag_app": tag_app, "timestamp": tagged_item.timestamp}, self.output)
        '''
        if item["timestamp"] <= self.last_timestamp:
            print "received an old timestamp, there is some issue in the item provider, ignore it. received:", item["timestamp"], ' previous:', self.last_timestamp
        else:
            #Ignore system auto app tag and folder tag
            if (not (item["tag"] in gDefaultAutoTagIgnoreTagsList)) and (not ("system:" in item["tag"])):
                if os.path.exists(item["full_path"]) and os.path.isdir(item["full_path"]):
                    '''
                    for folder_path, folders, filenames in os.walk(item["full_path"]):
                        for filename in filenames:
                            if filename in gDefaultAutoTagIgnoreFileList:
                                continue
                            target_full_path = os.path.join(folder_path, filename)
                            add_tag_for_full_path(target_full_path, item["tag"], gAutoTagServiceAppName)
                            if self.quit_flag:
                                break
                            time.sleep(1)
                        #########
                        # Ignore some folders
                        for ignore_folder in gDefaultAutoTagIgnoreFolderList:
                            if ignore_folder in folders:
                                folders.remove(ignore_folder)

                        if self.quit_flag:
                            break
                    '''
                    for path_name in os.listdir(item["full_path"]):
                        target_full_path = os.path.join(item["full_path"], path_name)
                        if os.path.isdir(target_full_path):
                            if path_name in gDefaultAutoTagIgnoreFolderList:
                                continue
                        else:
                            if path_name in gDefaultAutoTagIgnoreFileList:
                                continue
                        target_full_path = os.path.join(item["full_path"], path_name)
                        add_tag_for_full_path(target_full_path, item["tag"], gAutoTagServiceAppName)
                        if self.quit_flag:
                            break
                        time.sleep(1)


            if not self.quit_flag:
                #If quit, we are not sure if this element is processed, so do not update
                self.last_timestamp = item["timestamp"]
                param = self.get_state(self.diagram_id, {'all_tag_enum_start_timestamp': 0})
                param['all_tag_enum_start_timestamp'] = self.last_timestamp
                print 'set last timestamp', self.last_timestamp
                self.set_state(self.diagram_id, param)
            
            
        #Final return, default handler
        job.delete()
        return False#Do not need to put the item back to the tube
        

                


        
if __name__ == "__main__":
    s = SimpleService({
                            "input": "Input tube for generator",
                            #"output": "Output tube for generator",
                            #"session_id": "Used to identify this session, so previous session msg will be ignored", #now default in simple processor
                            #"diagram_id": "Each process diagram has an ID, it is used to save diagram related parameters", #now default in simple processor
                      },
                      thread_class = FolderTaggingThread)
    s.run()