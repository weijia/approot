import libsys
from libs.services.svc_base.managed_service import WorkerBase
#from libs.services.servicebase import service
#from django.conf import settings
#from ui_framework.objsys.models import UfsObj
#from tagging.models import Tag, TaggedItem
#import threading
#import traceback
#import libs.utils.transform as transform
import os
#import time
#import json
#import beanstalkc
#from configuration import g_config_dict
import traceback
os.environ["PATH"] = os.environ["PATH"]+";"+"C:\\Program Files (x86)\\Git\\bin"
from subprocess import (
                            call, 
                            Popen,
                            PIPE
                        )

import git
import win32con
from libs.services.svc_base.gui_service import GuiService
from libs.services.svc_base.simple_service_v2 import SimpleService


class GitPullerThread(WorkerBase):
    def pull_and_push_changes(self, branch, full_path, remote_branch, remote_repo):
        #print remote_branch#gitbucket/20130313_diagram_rewrite
        if branch.name in remote_branch.__str__():
            print 'remote commit: ', remote_branch.commit
            if branch.commit != remote_branch.commit:
                print 'different to remote'
                #Added istream to avoid error: WindowsError: [Error 6] The handle is invalid
                try:
                    print 'pulling changes'
                    remote_repo.pull(remote_branch.__str__().split('/')[-1],
                                     istream=PIPE)#20130313_diagram_rewrite
                    print 'latest remote log:', remote_branch.log()[-1].message
                except:
                    traceback.print_exc()
                try:
                    print 'pushing changes'
                    remote_repo.push(remote_branch.__str__().split('/')[-1],
                                     istream=PIPE)#20130313_diagram_rewrite
                    print 'latest local log:', branch.log()[-1].message
                except:
                    traceback.print_exc()
                GuiService().gui_msg(
                    "%s: %s updated: %s" % (full_path, branch.name, branch.log()[-1].message))

    def is_repo_ref_valid(self, remote_repo):
        #if hasattr(i, "refs"):
        #    print 'no refs attr'
        #print "length:", len(i.refs)
        is_ref_valid = True
        try:
            len(remote_repo.refs)
        except:
            is_ref_valid = False
        return is_ref_valid

    def is_ignored(self, url):
        if "https" in url:
            print 'ignoring :', url
            return True
        else:
            return False

    def process_remote_repo(self, branch, full_path, remote_repo):
        #Ignore https in company.
        if not self.is_ignored(remote_repo.url):
            try:
                if self.is_repo_ref_valid(remote_repo):
                    for remote_branch in remote_repo.refs:
                        self.pull_and_push_changes(branch, full_path, remote_branch, remote_repo)
            except:
                traceback.print_exc()

    def process_cur_session_msg(self, msg):
        full_path = msg.get_path()
        try:
            r = git.Repo(full_path)
            branch = r.active_branch
            print 'current branch:', branch.name, branch.commit

            for remote_repo in r.remotes:
                self.process_remote_repo(branch, full_path, remote_repo)
        except:
            traceback.print_exc()
        print 'item process done'
        return True

        
    
        
if __name__ == "__main__":
    s = SimpleService({
                            "input": "Input msg queue for path to pull and push",
                      },
                      worker_thread_class=GitPullerThread)
    s.run()