# -*- coding: gbk -*-
from django.utils.timezone import utc
import datetime
import json
import os
import shutil
import libsys
from libs.logsys.logSys import *
from django.conf import settings
from libs.services.svc_base.managed_service import WorkerBase
from libs.tagging.models import TaggedItem
from ui_framework.objsys.models import get_ufs_obj_from_full_path
from libs.utils.misc import ensureDir
from libs.utils.filetools import getFreeNameFromFullPath


class FileMover(WorkerBase):
    """
    没有Service结尾的作为worker thread
    """
    def worker_init(self):
        super(FileMover, self).worker_init()
        default_target = os.path.join(libsys.get_root_dir(), "../default_move_target/")
        self.target_dir = self.param_dict.get("target_path", default_target)
        ensureDir(self.target_dir)

    def process(self, msg):
        #Create the original object in UFS
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

        return True


from libs.services.svc_base.simple_service_v2 import SimpleService

if __name__ == "__main__":
    s = SimpleService({
                          "input": "Input msg queue for files to be moved",
                          "output": "Output msg queue for moved file notification",
                          "target_path": "Moving target for input files"
                      },
                      worker_thread_class=FileMover)
    s.run()
