import libsys
from libs.services.svc_base.managed_service import ManagedService
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

from libs.services.svc_base.simple_service_v2 import SimpleService

class ScacheStorageServiceApp(ManagedService):
    def process(self, msg):
        url = msg["url"]
        cached_path = msg["cached_path"]
        cached_path = transform.transformDirToInternal(cached_path)
        o = UfsObj.objects.filter(ufs_url=url)
        if 0 == o.count():
            s = UfsObj(ufs_url=url, full_path=cached_path)
            s.save()
        else:
            found = False
            for i in o:
                if i.full_path == cached_path:
                    #Already saved, ignore this storage
                    found = True
                    break
            if not found:
                s = UfsObj(ufs_url=url, full_path=cached_path)
                s.save()
        return True

if __name__ == "__main__":
    s = SimpleService({}, ScacheStorageServiceApp)
    s.run()