import sys
import os


def get_root_dir():
    c = os.getcwd()
    while c.find('approot') != -1:
        c = os.path.dirname(c)
    return os.path.join(c, 'approot')

sys.path.insert(0, get_root_dir())
