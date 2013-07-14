# -*- coding: gbk -*- 
"""
Created on 2012-02-13

@author: Richard
"""
import os
import time
import libsys
from libs.logsys.logSys import cl, info
from libs.services.svc_base.msg import Msg
from libs.services.svc_base.simple_service_v2 import SimpleService
from libs.services.svc_base.service_base import ThreadedService
import libs.utils.transform as transform


class FolderExpandThread(ThreadedService):
    def run(self):
        if os.path.isdir(self.task_info.get_path()):
            for i in os.walk(self.task_info.get_path()):
                #This will be set to True by external app
                if self.is_quitting():
                    break
                #Only send files
                for j in i[2]:
                    info(j)
                    full_path = transform.transformDirToInternal(os.path.join(i[0], j))
                    m = Msg({"folder": self.task_info.get_path()})
                    m.add_path(full_path)
                    self.send_to_output(m)
                    time.sleep(1)
        return True


if __name__ == "__main__":
    s = SimpleService({"full_path": "Full path of the folder need to expand", },
                      worker_thread_class=FolderExpandThread)
    s.run()