from libtool import include_root_path


class Config(object):
    def __getattr__(self):
        pass

include_root_path(__file__, "approot")
import configuration


def get_ufs_web_server_port():
    return configuration.g_config_dict["ufs_web_server_port"]


def get_postsql_server_port():
    return configuration.g_config_dict['POSTGRESQL_PORT']


def get_thumb_server_port():
    return configuration.g_config_dict.get("thumb_server_port", 8114)