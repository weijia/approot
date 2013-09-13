import libsys
from libs.platform.executor import execute_app_from_name_and_wait_for_complete
from libs.utils.filetools import findAppInProduct
from libs.services.svc_base.postgres_app import PostgreSqlApp
import configuration
import os
from django.contrib.auth.models import User, Group
from django.core.management.commands.syncdb import Command as SyncDb
try:
    from south.management.commands.syncdb import Command as SyncDb
except:
    pass
from south.management.commands.migrate import Command as Migrate
from django.db import DEFAULT_DB_ALIAS




if __name__ == "__main__":
    os.chdir(libsys.get_root_dir())
    PostgreSqlApp()
    #Check if initial database is OK. If it is not OK, syncdb.bat will be called.
    '''
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
    '''
    if False:
        '''
        try:
            anonymous_list = User.objects.filter(username="AnonymousUser")
            if 0 == anonymous_list.count():
                raise "bad"
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
        '''
    else:
        from django.db import connection
        connection.introspection.table_names()
        SyncDb().handle_noargs(**{"interactive": False, "verbosity": 1, "database": DEFAULT_DB_ALIAS, 'load_initial_data': False})
        #SyncDb().execute(noinput=True)#http://stackoverflow.com/questions/2772990/programmatically-sync-the-db-in-django
        #Migrate().handle_noargs(**{"interactive": False, "verbosity": 1, "database": DEFAULT_DB_ALIAS, 'load_initial_data': False})
        Migrate().handle()

    #thumb_port = configuration.g_config_dict.get("thumb_server_port", 8114)
    #execute_app_from_name_and_wait_for_complete("syncdb")
    execute_app_from_name_and_wait_for_complete("cherrypy_server")
    
    
    
    