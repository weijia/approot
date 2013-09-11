import os
import sys
####################################
def get_root_dir():
    c = os.getcwd()
    while c.find('approot') != -1:
        c = os.path.dirname(c)
    return os.path.join(c, 'approot')
    
root_dir = get_root_dir()
if not (root_dir in sys.path):
    sys.path.insert(0, get_root_dir())
#print sys.path

##################################
# Configurations
##################################

log_root = os.path.join(get_root_dir(), "../data/logs")


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

try:
    f = open('config.json', 'r')
    loaded_config = json.load(f)
except:
    #traceback.print_exc()
    print "no config file/ invalid config file, use default"
    
for i in g_config_dict:
    if loaded_config.has_key(i):
        g_config_dict[i] = loaded_config[i]
    os.environ[i] = str(g_config_dict[i])
    
os.environ["POSTGRESQL_ROOT"] = os.path.join(root_dir, "..\\others\\pgsql\\")
os.environ["CLASSPATH"] = os.path.join(root_dir, "..\\others\\scache\\src\\Beanstemc.jar")
os.environ["DJANGO_SETTINGS_MODULE"] = "rootapp.customized_settings"
###################################
try:
    os.mkdir(log_root)
    print "created dir:", log_root
except:
    pass

#Manually import these modules for build
import rootapp.separate_settings.build_settings
import rootapp.separate_settings.local_postgresql_settings