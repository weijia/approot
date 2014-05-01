import subprocess
from win32process import CREATE_NO_WINDOW
from libtool import find_root_path
from libtool.filetools import find_callable_in_app_framework
import sys
import os


def execute_app_from_name_and_wait_for_complete(app_name):
    app_path = find_callable_in_app_framework(app_name)
    #print "---------"+app_path
    if -1 != app_path.find(".py"):
        #print "------------"+sys.executable +" "+app_path
        os.system(sys.executable+" "+app_path)
    else:
        os.system(app_path)
    print "returning from app:"+sys.executable+" "+app_name


def execute_app(app_full_path, param_list=[], cur_working_dir=None):
    ext = os.path.splitext(app_full_path)[1]
    if cur_working_dir is None:
        cur_working_dir = find_root_path(__file__, "approot")

    if ".py" == ext:
        app_path_and_param_list = [sys.executable, '-u', app_full_path]
    else:
        app_path_and_param_list = [app_full_path]

    app_path_and_param_list.extend(param_list)

    if True:#try:
        if not os.path.exists(app_path_and_param_list[0]):
            print "path does not exist: ", app_path_and_param_list[0]
            #print subprocess.PIPE
        p = subprocess.Popen(app_path_and_param_list, cwd=cur_working_dir, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0, creationflags=CREATE_NO_WINDOW)
        return p
        #print "created pid:", p.pid