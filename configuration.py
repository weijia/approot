import logging
import os
import sys
import libs.root_lib_sys as root_lib

##################################
# Configurations
##################################

log_root = os.path.join(root_lib.get_root_dir(), "../data/logs")


gServerStartPort = 8110

import json
g_config_dict = {
    "ufs_web_server_port": gServerStartPort,
    "ufs_sftp_server_port": gServerStartPort+1,
    "ufs_beanstalkd_port": gServerStartPort+2,
    "POSTGRESQL_PORT": gServerStartPort+3,
    "drop_wnd_color": None,
    "thumb_server_port": gServerStartPort+4,
}
import traceback
loaded_config = {}

import libtool


try:
    f = open(os.path.join(libtool.get_file_folder(__file__), 'config.json'), 'r')
    loaded_config = json.load(f)
except:
    #traceback.print_exc()
    logging.warn("no config file/ invalid config file, use default")
    
for i in g_config_dict:
    if loaded_config.has_key(i):
        g_config_dict[i] = loaded_config[i]
    os.environ[i] = str(g_config_dict[i])
    
os.environ["POSTGRESQL_ROOT"] = os.path.join(root_lib.get_root_dir(), "..\\others\\pgsql\\")
os.environ["CLASSPATH"] = os.path.join(root_lib.get_root_dir(), "..\\others\\scache\\src\\Beanstemc.jar")

###################################
try:
    os.mkdir(log_root)
    print "created dir:", log_root
except:
    pass


def get_default_charset():
    from extra_settings.init_settings import init_settings

    django_auto_conf = init_settings()
    settings = django_auto_conf.get_settings()
    try:
        return settings.DEFAULT_CHARSET
    except:
        return "utf8"