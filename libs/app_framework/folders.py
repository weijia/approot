import libsys
from libs.utils.misc import ensure_dir
import os


def get_or_create_app_data_folder(folder_name):
    app_data_folder = os.path.join(libsys.get_root_dir(), "../%s/" % folder_name)
    ensure_dir(app_data_folder)
    return app_data_folder

