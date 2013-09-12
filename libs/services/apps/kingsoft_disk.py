# -*- coding: gbk -*-
from django.utils.timezone import utc
#import datetime
#import json
import os
#import shutil
from urllib2 import HTTPError
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

jinshan_root = os.path.join(libsys.get_root_dir(), "libs/jinshankuaipan/")
sys.path.insert(0, jinshan_root)

from libs.jinshankuaipan.kuaipan import KuaiPan


class KingsoftDisk(SimpleServiceWorker, StatefulProcessor):
    AUTHORIZE_NOT_STARTED = 0
    AUTHORIZE_BEFORE_GETTING_ACCESS_TOKEN = 1
    AUTHORIZED = 5

    def on_register_ok(self):
        super(KingsoftDisk, self).on_register_ok()
        self.failed_cnt = 0
        self.kp = KuaiPan()
        state = self.get_state(self.get_task_signature(), {})
        if ("oauth_token" in state) and ("oauth_token_secret" in state):
            #self.authorize_state = self.AUTHORIZE_BEFORE_GETTING_ACCESS_TOKEN
            self.authorize_state = self.AUTHORIZED
            #self.oauth_token = state["oauth_token"]
            self.kp.oauth_token = state["oauth_token"].encode('utf8')
            print "token", self.kp.oauth_token
            self.kp.oauth_token_secret = state["oauth_token_secret"].encode('utf8')
            print self.kp.oauth_token_secret
            cl(self.kp.account_info())
        else:
            self.oauth_token = None
            #self.authorize_state = self.AUTHORIZE_NOT_STARTED
            self.get_request_token()

    def get_access_token(self):
        print "access token:", self.oauth_token
        self.token = self.kp.accessToken(self.oauth_token)
        print 'oauth_token', self.token["oauth_token"]
        print 'oauth_token_secret', self.token['oauth_token_secret']
        print self.kp.account_info()
        try:
            self.kp.create_folder("ufs")
        except:
            traceback.print_exc()
        #Save access token
        state = self.get_state(self.get_task_signature(), {})
        state["oauth_token"] = self.token["oauth_token"]
        state["oauth_token_secret"] = self.token['oauth_token_secret']
        self.set_state(self.get_task_signature(), state)
        self.authorize_state = self.AUTHORIZED

    def get_request_token(self):
        #self.kp = KuaiPan()
        self.tempToken = self.kp.requestToken()
        self.authLink = self.kp.authorize(self.tempToken["oauth_token"])
        #self.gui_service = GuiService()
        #self.gui_service.put({"command": "Browser",
        #              "url": self.authLink,
        #              "handle": "kuaipan"})
        os.startfile(self.authLink)
        self.authorize_state = self.AUTHORIZE_BEFORE_GETTING_ACCESS_TOKEN

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
            self.kp.upload(basename, obj.full_path, root="app_folder/ufs")
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
                      worker_thread_class=KingsoftDisk)
    s.run()