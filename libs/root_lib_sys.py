import sys
import os


def get_root_dir():
    c = os.getcwd()
    while c.find('approot') != -1:
        c = os.path.dirname(c)
    return os.path.join(c, 'approot')


def insert_lib_dirs(lib_list):
    for i in lib_list:
        if not (os.path.join(get_root_dir(), i) in sys.path):
            sys.path.insert(0, i)


insert_lib_dirs(["libs", "ui_framework"])