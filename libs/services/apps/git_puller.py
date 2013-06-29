import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread, beanstalkServiceApp
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
from libs.services.svc_base.simpleservice import SimpleService


class GitPullerServiceApp(beanstalkServiceApp):
    def procCurSessionItem(self, job, item):
        if item.has_key("input"):
            self.beanstalk.watch(item["input"])
            '''
            #The following part will be done in processItem
            job.delete()
            return False
            '''
        fullpath = item["full_path"]
        try:
            r = git.Repo(fullpath)
            branch = r.active_branch
            print 'current branch:', branch.name, branch.commit

            for i in r.remotes:
                #Ignore https in company.
                if "https" in i.url:
                    print 'ignoring :', i.url
                    continue
                try:
                    #if hasattr(i, "refs"):
                    #    print 'no refs attr'
                    #print "length:", len(i.refs)
                    try:
                        len(i.refs)
                    except:
                        continue
                    for remote_branch in i.refs:
                        #print remote_branch#gitbucket/20130313_diagram_rewrite
                        if branch.name in remote_branch.__str__():
                            print 'remote commit: ', remote_branch.commit
                            if branch.commit != remote_branch.commit:
                                print 'different to remote'
                                #Added istream to avoid error: WindowsError: [Error 6] The handle is invalid
                                try:
                                    print 'pulling changes'
                                    i.pull(remote_branch.__str__().split('/')[-1], istream=PIPE)#20130313_diagram_rewrite
                                    print 'latest remote log:', remote_branch.log()[-1].message
                                except:
                                    traceback.print_exc()
                                try:
                                    print 'pushing changes'
                                    i.push(remote_branch.__str__().split('/')[-1], istream=PIPE)#20130313_diagram_rewrite
                                    print 'latest local log:', branch.log()[-1].message
                                except:
                                    traceback.print_exc()
                                GuiService().gui_msg("%s: %s updated: %s"%(fullpath, branch.name, branch.log()[-1].message))
                except:
                    traceback.print_exc()
        except:
            traceback.print_exc()
        print 'item process done'
        '''
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True
        '''


        
    
        
if __name__ == "__main__":
    s = SimpleService({
                            "input":"Input tube for path to pull", 
                      },
                      GitPullerServiceApp)
    s.run()