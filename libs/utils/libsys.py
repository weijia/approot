import sys
import os


def get_root_dir():
    c = os.getcwd()
    while c.find('approot') != -1:
        c = os.path.dirname(c)
    return os.path.join(c, 'approot')

if not (get_root_dir() in sys.path):
    sys.path.insert(0, get_root_dir())

try:
    #This is used for approot only
    import libs.root_lib_sys
except:
    pass
