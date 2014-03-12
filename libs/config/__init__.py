from libtool import include_root_path


class Config(object):
    def __getattr__(self):
        pass

include_root_path(__file__, "approot")
from configuration import g_config_dict, get_default_charset

from configuration import get_default_charset

def get_ufs_web_server_port():
    g_config_dict["ufs_web_server_port"]