import sys
from libs.utils.filetools import findAppInProduct
import libsys
from libs.services.svc_base.postgres_app import PostgreSqlApp
import configuration
import os
from django.contrib.auth.models import User, Group


if __name__ == "__main__":
    os.chdir(libsys.get_root_dir())
    PostgreSqlApp()
    #Check if initial database is OK. If it is not OK, syncdb.bat will be called.
    flag_file = os.path.join(libsys.get_root_dir(), "syncdb_needed.txt")
    try:
        anonymous_list = User.objects.filter(username="AnonymousUser")
        if 0 == anonymous_list.count():
            raise "bad"
        if os.path.exists(flag_file):
            os.remove(flag_file)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        #print "set SYNCDB flag"
        #os.environ["SYNCDB"] = "YES"
        if not os.path.exists(flag_file):
            open(flag_file, "w").close()

    thumb_port = configuration.g_config_dict.get("thumb_server_port", 8114)
    os.system(findAppInProduct("syncdb"))
    os.system(sys.executable+" "+findAppInProduct("cherrypy_server"))
    
    
    
    