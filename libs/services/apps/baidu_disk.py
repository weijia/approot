# -*- coding: gbk -*-
from django.utils.timezone import utc
#import datetime
#import json
import os
#import shutil
from urllib2 import HTTPError


import libsys
import configuration
from libs.utils.obj_tools import get_ufs_obj_from_full_path
from configuration import *
from django.conf import settings
from social_auth.db.django_models import UserSocialAuth
from libs.services.svc_base.state import StatefulProcessor
from libs.services.svc_base.gui_service import GuiService
from libs.logsys.logSys import *


#from libs.services.svc_base.managed_service import WorkerBase
from libs.tagging.models import TaggedItem
#from libs.utils.misc import ensureDir
#from libs.utils.filetools import getFreeNameFromFullPath
from libs.services.svc_base.simple_service_v2 import SimpleService, SimpleServiceWorker
import traceback

jinshan_root = os.path.join(libsys.get_root_dir(), "libs/jinshankuaipan/")
sys.path.insert(0, jinshan_root)

from baidu_pcs.baidu_pcs import Client as BaiduClient


class BaiduDisk(SimpleServiceWorker, StatefulProcessor):
    AUTHORIZE_NOT_STARTED = 0
    AUTHORIZE_BEFORE_GETTING_ACCESS_TOKEN = 1
    AUTHORIZED = 5

    def set_storage(self):
        print UserSocialAuth.objects.filter(provider='baidu')[0].extra_data
        self.state = UserSocialAuth.objects.filter(provider='baidu')[0].extra_data
        self.storage = BaiduClient(self.state["access_token"])
        #result = self.storage.mkdir("/apps/")
        #print result
        try:
            result = self.storage.mkdir("/apps/ufs_django/ufs/")
            print result
        except:
            pass

        #self.authorize_state = self.AUTHORIZED

    def is_authorized_in_baidu(self):
        #return False
        return 0 != UserSocialAuth.objects.filter(provider='baidu').count()

    def start_auth(self):
        self.storage = None
        #self.authorize_state = self.AUTHORIZE_BEFORE_GETTING_ACCESS_TOKEN
        authLink = 'http://127.0.0.1:%d/login/baidu/' % configuration.g_config_dict["ufs_web_server_port"]
        os.startfile(authLink)

    def on_register_ok(self):
        super(BaiduDisk, self).on_register_ok()
        self.invalid_auth_list = []
        self.current_auth = 0

        self.failed_cnt = 0
        if self.is_authorized_in_baidu():
            self.set_storage()
        else:
            self.start_auth()

    def process(self, msg):
        if not self.is_authorized_in_baidu():
            self.start_auth()
            #Put the file back
            self.put(msg, 30)
        else:
            #Create the original object in UFS
            if os.path.exists(msg.get_path()):
                self.upload_file_in_msg(msg)
            else:
                cl("File does not exist: %s" % msg.get_path())
        return True

    def upload_file_in_msg(self, msg):
        obj = get_ufs_obj_from_full_path(msg.get_path())
        basename = os.path.basename(obj.full_path)
        try:
            result = self.storage.upload_single("/apps/ufs_django/ufs/"+basename, obj.full_path, ondup='newcopy')
            print result
            self.gui_service = GuiService()
            self.gui_service.put({"command": "notify",
                                  "msg": "File %s uploaded. result: %s" % (obj.full_path, result)})
            self.failed_cnt = 0
            #cl("File uploaded successfully")
        except HTTPError, e:
            print e
            if 401 == e.code:
                # Unauthorized
                self.put(msg, 30)
                #self.authorize_state = self.AUTHORIZE_NOT_STARTED
                state = self.get_state(self.get_task_signature(), {"oauth_token": None})
                del state["oauth_token"]
                #state["oauth_token_secret"] = self.token['oauth_token_secret']
                self.set_state(self.get_task_signature(), state)
            elif 405 == e.code:
                print "not allowed, possibly same name exists"
            else:
                raise
        finally:
            traceback.print_exc()
            #cl("File upload failed will retry")


if __name__ == "__main__":
    s = SimpleService({
                          "input": "Input msg queue for files to be moved"
                      },
                      worker_thread_class=BaiduDisk)
    s.run()