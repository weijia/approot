import os
from libtool import find_root_even_frozen, include_root_path
from libtool.filetools import get_free_timestamp_filename_in_path
from ufs_utils.misc import ensure_dir

include_root_path(__file__, "approot")
import configuration

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
        return "127.0.0.1:" + str(ConfStorage.get_ufs_web_server_port())

    @staticmethod
    def get_ufs_web_server_port():
        return configuration.g_config_dict["ufs_web_server_port"]