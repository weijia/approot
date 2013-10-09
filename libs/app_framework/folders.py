import libsys
from libs.utils.misc import ensure_dir
import os


def get_or_create_app_data_folder(folder_name):
    app_data_folder = os.path.join(libsys.get_root_dir(), "../%s/" % folder_name)
    ensure_dir(app_data_folder)
    return app_data_folder


def get_app_in_framework(folder, name):
    other_app_full_path = os.path.abspath(os.path.join(libsys.get_root_dir(), "../others/%s" % folder))
    full_path = os.path.join(other_app_full_path, name)
    if os.path.exists(full_path):
        return full_path
    print full_path
    raise "Not exist"


def get_app_full_path_by_name(name):
    if "7z" == name:
        try:
            return get_app_in_framework("7z", "7za.exe")
        except:
            return get_app_in_framework("7za920", "7za.exe")