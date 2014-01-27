from libs.utils.filetools import find_callable_in_app_framework
import sys
import os


def execute_app_from_name_and_wait_for_complete(app_name):
    app_path = find_callable_in_app_framework(app_name)
    #print "---------"+app_path
    if -1 != app_path.find(".py"):
        #print "------------"+sys.executable +" "+app_path
        os.system(sys.executable+" "+app_path)
    os.system(app_path)
