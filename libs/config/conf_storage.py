import os
from libtool import find_root_even_frozen
from libtool.filetools import get_free_timestamp_filename_in_path
from ufs_utils.misc import ensure_dir


class ConfStorage(object):
    @staticmethod
    def get_free_name_for_exported_data(prefix=''):
        exported_root_path = ConfStorage.get_root_path_for_exported_data()
        ensure_dir(exported_root_path)
        return get_free_timestamp_filename_in_path(exported_root_path, ".json", prefix)

    @staticmethod
    def get_root_path_for_exported_data():
        return os.path.join(find_root_even_frozen("approot"), "../obj_exported/")

    @staticmethod
    def get_ufs_server_and_port_str():
        return "http://127.0.0.1:8210"