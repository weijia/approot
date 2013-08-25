# -*- coding: gbk -*-
from django.utils.timezone import utc
#import datetime
#import json
import json
import os
#import shutil
from urllib2 import HTTPError
from libs.social_auth.db.django_models import UserSocialAuth
import libsys
from libs.services.svc_base.state import StatefulProcessor
from libs.services.svc_base.gui_service import GuiService
from libs.logsys.logSys import *
from django.conf import settings
#from libs.services.svc_base.managed_service import WorkerBase
from libs.tagging.models import TaggedItem
#from libs.utils.misc import ensureDir
#from libs.utils.filetools import getFreeNameFromFullPath
from libs.services.svc_base.simple_service_v2 import SimpleService, SimpleServiceWorker
import traceback
from ui_framework.objsys.local_obj_tools import get_ufs_obj_from_full_path

jinshan_root = os.path.join(libsys.get_root_dir(), "libs/jinshankuaipan/")
sys.path.insert(0, jinshan_root)

from libs.baidu_pcs.pcs import Client as BaiduClient


class BaiduDisk(SimpleServiceWorker, StatefulProcessor):
    AUTHORIZE_NOT_STARTED = 0
    AUTHORIZE_BEFORE_GETTING_ACCESS_TOKEN = 1
    AUTHORIZED = 5

    def on_register_ok(self):
        super(BaiduDisk, self).on_register_ok()
        self.failed_cnt = 0
        state = self.get_state(self.get_task_signature(), {})
        if "access_token" in state:
            self.storage = BaiduClient(state["access_token"])
        else:
            self.storage = None
            authLink = 'http://localhost:8110/login/baidu/'
            os.startfile(authLink)

    def get_access_token(self):
        state = json.loads(UserSocialAuth.objects.filter()[0].extra_data)
        self.set_state(self.get_task_signature(), state)
        self.authorize_state = self.AUTHORIZED
        self.storage = BaiduClient(state["access_token"])

    def process(self, msg):
        if self.authorize_state == self.AUTHORIZE_BEFORE_GETTING_ACCESS_TOKEN:
            try:
                self.get_access_token()
            except:
                traceback.print_exc()

        if self.authorize_state == self.AUTHORIZED:
            #Create the original object in UFS
            if os.path.exists(msg.get_path()):
                self.upload_file_in_msg(msg)
            else:
                cl("File does not exist: %s" % msg.get_path())
        else:
            if self.authorize_state == self.AUTHORIZE_NOT_STARTED:
                self.get_request_token()

            #Put the file back
            self.put(msg, 30)
        return True

    def upload_file_in_msg(self, msg):
        obj = get_ufs_obj_from_full_path(msg.get_path())
        basename = os.path.basename(obj.full_path)
        try:
            self.storage.upload_single("app_folder/ufs", obj.full_path, ondup=newcopy)
            self.gui_service = GuiService()
            self.gui_service.put({"command": "notify",
                                  "msg": "File %s uploaded." % obj.full_path})
            self.failed_cnt = 0
            #cl("File uploaded successfully")
        except HTTPError, e:
            print e
            if 401 == e.code:
                # Unauthorized
                self.put(msg, 30)
                self.authorize_state = self.AUTHORIZE_NOT_STARTED
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