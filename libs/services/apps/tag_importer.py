import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread, beanstalkServiceApp
from libs.services.servicebase import service
from django.conf import settings
from ui_framework.objsys.models import UfsObj
from libs.tagging.models import Tag, TaggedItem
import threading
import traceback
import json
import time
import datetime
from django.utils.timezone import utc
import uuid
import os
from libs.logsys.logSys import *
import libs.utils.obj_tools as objtools
from libs.services.svc_base.simpleservice import SimpleService
from libs.utils.misc import ensureDir as ensure_dir
from libs.services.svc_base.state import StatefulProcessor

gTagImporterProcessorId = '90843930-0481-4106-8ec8-c7bb1f508f4b'



class TagImporter(beanstalkServiceApp, StatefulProcessor):
    def startServer(self):
        root_dir = libsys.get_root_dir()
        dump_root = os.path.join(root_dir, "../tag_dump_import/")
        ensure_dir(dump_root)

        param = self.get_state(gTagImporterProcessorId, {"timestamp": 0})
        if True:
            last_timestamp = param["timestamp"]
            print last_timestamp
            
            for filename in os.listdir(dump_root):
                cur_timestamp = float(filename.replace('.json', ''))
                if cur_timestamp > last_timestamp:
                    file = open(os.path.join(dump_root, filename), 'r')
                    data = json.load(file)
                    for i in data:
                        cl(i)
                        ufs_url=i["ufs_url"]
                        if i.has_key("uuid"):
                            obj_uuid = i["uuid"]
                        else:
                            obj_uuid = unicode(uuid.uuid4())
                        is_local = False
                        if objtools.isUfsFs(ufs_url):
                            #Normally we will always come to here
                            is_local = objtools.is_local(ufs_url)
                            full_path = objtools.getPathForUfsUrl(ufs_url)
                        else:
                            #Temp support legacy url
                            #In file:///D:/xxx/xxx.xxx format
                            full_path = objtools.get_full_path_for_local_os(ufs_url)
                            ufs_url = objtools.getUfsUrlForPath(full_path)
                            is_local = True
                        #obj_list_from_full_path = UfsObj.objects.filter(full_path = full_path)
                        obj_list = UfsObj.objects.filter(ufs_url = ufs_url)
                        if 0 == obj_list.count():
                            if is_local:
                                obj = UfsObj(ufs_url = ufs_url, full_path=full_path, uuid = obj_uuid)
                            else:
                                obj = UfsObj(ufs_url = ufs_url, uuid = obj_uuid)
                            obj.save()
                        else:
                            obj = obj_list[0]
                        
                        #Create tags for object
                        '''
                        all_tags = []
                        for existing_tag in obj.tags:
                            all_tags.append(existing_tag)
                            
                        all_tags.extend(i["tags"])
                        
                        obj.tags = ','.join(all_tags)
                        
                        cl('applying : ', i["ufs_url"], i["tags"])
                        '''
                        
                        for new_tag in i["tags"]:
                            if type(new_tag) == dict:
                                one_tag = new_tag["tag"]
                                tag_app = new_tag["app"]
                            else:
                                one_tag = new_tag
                                tag_app = None
                            Tag.objects.add_tag(obj, one_tag, tag_app)
                        
                        if self.quit_flag:
                            break
                    if self.quit_flag:
                        break
                    time.sleep(1)
                    last_timestamp = cur_timestamp
        
        ######
        # Quitting, so save last_timestamp
        param["timestamp"] = last_timestamp
        self.set_state(gTagImporterProcessorId, param)
                
        
    
        
if __name__ == "__main__":
    s = SimpleService({
                            "input": "Input tube for generator",
                            "output": "Output tube for generator",
                      },
                      TagImporter)
    s.run()