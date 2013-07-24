# -*- coding: gbk -*-
from django.utils.timezone import utc
import datetime
import json
import os
import shutil
import libsys
from libs.logsys.logSys import *
from django.conf import settings
#from libs.services.svc_base.managed_service import WorkerBase
from libs.tagging.models import TaggedItem
from ui_framework.objsys.models import get_ufs_obj_from_full_path
from libs.utils.misc import ensureDir
from libs.utils.filetools import getFreeNameFromFullPath
from libs.services.svc_base.simple_service_v2 import SimpleService, SimpleServiceWorker

class FileMover(SimpleServiceWorker):
    """
    没有Service结尾的作为worker thread
    """
    def on_register_ok(self):
        super(FileMover, self).on_register_ok()
        default_target = os.path.join(libsys.get_root_dir(), "../default_move_target/")
        self.target_dir = self.param_dict.get("target_path", default_target)
        ensureDir(self.target_dir)

    def process(self, msg):
        #Create the original object in UFS
        if os.path.exists(msg.get_path()):
            obj = get_ufs_obj_from_full_path(msg.get_path())
            basename = os.path.basename(obj.full_path)
            target_path = os.path.abspath(os.path.join(self.target_dir, basename))
            if os.path.exists(target_path):
                target_path = getFreeNameFromFullPath(target_path)

            cl("moving from: %s to %s" % (obj.full_path, target_path))
            shutil.move(obj.full_path, target_path)

            #Create a tracking for the moving
            description = json.loads(obj.description)
            moved_to = description.get("moved_to", [])
            moved_to.append(target_path)
            description["moved_to"] = moved_to
            obj.description = json.dumps(description)
            obj.save()

            #Create the new object in database
            new_obj = get_ufs_obj_from_full_path(target_path)
            target_tags = []
            for tag in obj.tags:
                target_tags.append(tag.name)
            #cl("!!!!!!!!!!!!!!!!! Is it OK for tags? %s" % ",".join(obj.tags))
            new_obj.tags = ",".join(target_tags)
        else:
            cl("File does not exist: %s" % msg.get_path())
        return True


if __name__ == "__main__":
    s = SimpleService({
                          "input": "Input msg queue for files to be moved",
                          "output": "Output msg queue for moved file notification",
                          "target_path": "Moving target for input files"
                      },
                      worker_thread_class=FileMover)
    s.run()