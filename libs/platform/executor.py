from libs.utils.filetools import findAppInProduct
import sys
import os


def execute_app_from_name_and_wait_for_complete(app_name):
    app_path = findAppInProduct(app_name)
    if -1 != app_path.find(".py"):
        os.system(sys.executable+" "+app_path)
    os.system(app_path)
