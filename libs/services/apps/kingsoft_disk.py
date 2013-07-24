# -*- coding: gbk -*-
from django.utils.timezone import utc
#import datetime
#import json
import os
#import shutil
import libsys
from libs.services.svc_base.gui_service import GuiService

from libs.logsys.logSys import *
from django.conf import settings
#from libs.services.svc_base.managed_service import WorkerBase
from libs.tagging.models import TaggedItem
from ui_framework.objsys.models import get_ufs_obj_from_full_path
#from libs.utils.misc import ensureDir
#from libs.utils.filetools import getFreeNameFromFullPath
from libs.services.svc_base.simple_service_v2 import SimpleService, SimpleServiceWorker


jinshan_root = os.path.join(libsys.get_root_dir(), "libs/jinshankuaipan/")
sys.path.insert(0, jinshan_root)

from libs.jinshankuaipan.kuaipan import KuaiPan


class KingsoftDisk(SimpleServiceWorker):
    AUTHORIZE_NOT_STARTED = 0
    AUTHORIZE_PAGE_OPENED_STATE = 1
    AUTHORIZED = 5

    def worker_init(self):
        super(KingsoftDisk, self).worker_init()
        #self.is_authorized = False
        self.authorize_state = self.AUTHORIZE_NOT_STARTED

    def process(self, msg):
        if self.authorize_state == self.AUTHORIZE_PAGE_OPENED_STATE:
            self.token = self.kp.accessToken()
            print 'oauth_token', self.token["oauth_token"]
            print 'oauth_token_secret', self.token['oauth_token_secret']
            print self.kp.account_info()
            self.kp.create_folder("UfsAutoCreated")
            self.authorize_state = self.AUTHORIZED

        if self.authorize_state == self.AUTHORIZED:
            #Create the original object in UFS
            if os.path.exists(msg.get_path()):
                obj = get_ufs_obj_from_full_path(msg.get_path())
                basename = os.path.basename(obj.full_path)
                self.kp.upload(basename, obj.full_path)
                cl("File uploaded successfully")
            else:
                cl("File does not exist: %s" % msg.get_path())
        else:
            if self.authorize_state == self.AUTHORIZE_NOT_STARTED:
                self.kp = KuaiPan()
                self.tempToken = self.kp.requestToken()
                self.authLink = self.kp.authorize(self.tempToken["oauth_token"])
                #self.gui_service = GuiService()
                #self.gui_service.put({"command": "Browser",
                #              "url": self.authLink,
                #              "handle": "kuaipan"})
                os.startfile(self.authLink)
                self.authorize_state = self.AUTHORIZE_PAGE_OPENED_STATE

            #Put the file back
            self.put(msg, 300)
        return True


if __name__ == "__main__":
    s = SimpleService({
                          "input": "Input msg queue for files to be moved"
                      },
                      worker_thread_class=KingsoftDisk)
    s.run()