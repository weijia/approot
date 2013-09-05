from libs.services.external_app.postgres_app import PostgreSqlApp
import libsys
from libs.services.svc_base.launcher_interface import Launcher
import configuration
import libs.utils.filetools as fileTools
import psycopg2
import sys
import os
from libs.utils.process_mgr import gProcessMgr
from django.contrib.auth.models import User, Group




def wait_for_app(app_and_param_list):
    name = app_and_param_list[0]
    app_full_path = fileTools.findAppInProduct(name)
    if app_full_path is None:
        print name
        raise "Path not find"
    app_full_path_and_param_list = [app_full_path]
    app_full_path_and_param_list.extend(app_and_param_list[:1])
    cur_working_dir = libsys.get_root_dir()
    gProcessMgr().wait_for_complete_without_console(app_full_path_and_param_list, cur_working_dir)





class MongoDbApp(ExtAppMgrIntf):
    def __init__(self):
        ###########################
        # Start mongodb
        ###########################
        start_app_shortcut('mongodb')

        #Check if mongodb started correctly
        retry_cnt = 0
        from pymongo import Connection
        from pymongo.errors import AutoReconnect

        while True:
            try:
                connection = Connection()
                break
            except AutoReconnect:
                retry_cnt += 1
                if retry_cnt > 40:
                    print "mongodb start failed"
                    break


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
    except:
        #print "set SYNCDB flag"
        #os.environ["SYNCDB"] = "YES"
        if not os.path.exists(flag_file):
            open(flag_file, "w").close()

    thumb_port = configuration.g_config_dict.get("thumb_server_port", 8114)
    #Start thumb server
    #Launcher().start_app_with_name_no_wait("managed_cherrypy_server", ["--port", "%d" % thumb_port])
    #Other initial apps need to be launched may be added to initial_launcher
    #print 'POSTGRESQL_PORT:', os.environ.get("POSTGRESQL_PORT")
    #start_app_shortcut("start_ext")
    #sys.stdout.flush()
    #wait_for_app(["start_ext"])
    #wait_for_app(["runserver"])
    #start_app_shortcut("tagging")
    #The following is not working as tube logging service is not started automatically currently
    #start_app_shortcut("tube_logging_service", ["--input", "ufs_test_tube"])
    from libs.services.apps.managed_cherrypy_server import main
    main()
    
    
    
    