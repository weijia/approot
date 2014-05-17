import zipfile
from libtool import include_sub_folder_in_root_path
include_sub_folder_in_root_path(__file__, "approot", "libs")
import configuration
from extra_settings.init_settings import init_settings
__inited_setting = init_settings()

import os


default_os_list_dir = None


def cx_freeze_list_dir(dirname):
    formatted = dirname.replace("\\", "/")
    lib_filename = "library.zip"
    if ("/%s/" % lib_filename) in formatted:
        lib_filename_index = formatted.find(lib_filename)
        lib_path = formatted[0:lib_filename_index]+lib_filename
        inner_path = formatted[lib_filename_index+len(lib_filename)+1:]
        zz = zipfile.ZipFile(lib_path)
        res = []
        #f = open("g:\\log.txt", "w")
        for name in zz.namelist():
            if inner_path.replace("\\", "/") in name:
                final = name.replace(inner_path, "").replace(".pyc", ".py")
                print '%s' % final
                #f.write(final+"\r\n")
                res.append(final[1:])
        zz.close()
        #f.close()
        #print "returning: ", res
        return res
    return default_os_list_dir(dirname)


default_os_list_dir = os.listdir
os.listdir = cx_freeze_list_dir


try:
    from django_commands_dict import django_commands_dict
except ImportError:
    django_commands_dict = None
