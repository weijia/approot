import sys
import os


def insert_lib_dirs(lib_list):
    for i in lib_list:
        if not (i in sys.path):
            sys.path.insert(0, i)

insert_lib_dirs(["libs", "ui_framework"])