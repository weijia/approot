import os
from iconizer.iconizer_main import Iconizer
import libsys
from libs.app_framework.folders import get_or_create_app_data_folder
from libs.utils.filetools import find_callable_in_app_framework
from libs.platform.executor import execute_app_from_name_and_wait_for_complete

from libs.services.svc_base.postgres_app import PostgreSqlApp
#The following will set environment string for start web server.
import configuration

from django.core.management.commands.syncdb import Command as SyncDb
try:
    from south.management.commands.syncdb import Command as SyncDb
except:
    pass
from south.management.commands.migrate import Command as Migrate
from django.db import DEFAULT_DB_ALIAS
from django.db import connection
import django.core.management as core_management


def sync_migrate_db():
    #Check if initial database is OK. If it is not OK, syncdb.bat will be called.
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
        print connection.introspection.table_names()
        #_commands = []
        '''
        {'clean_nonces': 'social_auth', 'compilemessages': 'django.core', 'dumpdata': 'django.core',
         'startproject': 'django.core', 'cleanupregistration': 'registration', 'findstatic': 'django.contrib.staticfiles',
          'loaddata': 'django.core', 'createcachetable': 'django.core', 'flush': 'django.core', 'syncdb': 'south',
           'convert_to_south': 'south', 'sqlinitialdata': 'django.core', 'migrationcheck': 'south', 'runserver': 'django.contrib.staticfiles',
           'migrate': 'south', 'dbshell': 'django.core', 'clean_associations': 'social_auth', 'runfcgi': 'django.core', 'test': 'south',
           'datamigration': 'south', 'sqlclear': 'django.core', 'changepassword': 'django.contrib.auth', 'sqlreset': 'django.core', 'shell': 'django.core',
            'sqlsequencereset': 'django.core', 'testserver': 'south', 'makemessages': 'django.core', 'schemamigration': 'south', 'graphmigrations': 'south',
             'startmigration': 'south', 'sql': 'django.core', 'validate': 'django.core', 'sqlall': 'django.core', 'collectstatic': 'django.contrib.staticfiles',
             'reset': 'django.core', 'diffsettings': 'django.core', 'inspectdb': 'django.core', 'startapp': 'django.core', 'createsuperuser': 'django.contrib.auth',
             'sqlflush': 'django.core', 'sqlcustom': 'django.core', 'cleanup': 'django.core', 'sqlindexes': 'django.core'}

        '''
        #from django.core.management import get_commands
        #print get_commands()
        #print _commands
        print 'setting commands', core_management._commands
        core_management._commands = {"syncdb": "django.core", "migrate": "south", "loaddata": "django.core"}
        print core_management._commands
        SyncDb().handle_noargs(
            **{"interactive": False, "verbosity": 1, "database": DEFAULT_DB_ALIAS, 'load_initial_data': False})
        print '-----------------------------'
        print core_management._commands

        #Migrate().handle_noargs(**{"interactive": False, "verbosity": 1, "database": DEFAULT_DB_ALIAS, 'load_initial_data': False})
        Migrate().handle()


if __name__ == "__main__":
    os.chdir(libsys.get_root_dir())
    PostgreSqlApp()

    sync_migrate_db()
    log_folder = get_or_create_app_data_folder("logs")
    i = Iconizer(log_folder)
    i.execute({"startBeanstalkd": [find_callable_in_app_framework("startBeanstalkd")]})
    i.execute({"msg_based_service_mgr": [find_callable_in_app_framework("msg_based_service_mgr")]})
    #thumb_port = configuration.g_config_dict.get("thumb_server_port", 8114)
    #execute_app_from_name_and_wait_for_complete("syncdb")
    execute_app_from_name_and_wait_for_complete("cherrypy_server")
    print "-----------------------------exiting cherrypy server"
    
    
    
    