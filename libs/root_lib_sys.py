import sys
import os


def get_root_dir(root_dir_name='approot'):
    c = os.getcwd()
    while c.find(root_dir_name) != -1:
        c = os.path.dirname(c)
    return os.path.join(c, root_dir_name)


def insert_lib_dir(lib_dir):
    dir_full_path = os.path.abspath(os.path.join(get_root_dir(), lib_dir))
    if not (dir_full_path in sys.path):
        sys.path.insert(0, lib_dir)


def insert_lib_dirs(lib_list):
    for i in lib_list:
        insert_lib_dir(i)


insert_lib_dirs(["libs", "ui_framework"])