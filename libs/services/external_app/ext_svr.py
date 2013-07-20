import libsys
import configuration
import libs.utils.filetools as fileTools
import psycopg2
import sys
import os
from libs.services.svc_base.gui_service import GuiService
from libs.utils.process_mgr import gProcessMgr

class ExtAppMgrIntf(object):
    def __init__(self):
        pass

    def check_complet(self):
        pass

    def shutdown(self):
        pass


def start_app_shortcut(app_name, param = []):
    #print "-------------------------", os.environ["POSTGRESQL_ROOT"]
    gui_service = GuiService()
    gui_service.put({"command": "LaunchApp", "app_name": app_name, "param": param})


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


class PostgreSqlApp(ExtAppMgrIntf):
    def __init__(self):
        ###########################
        # Start postgresql
        ###########################
        start_app_shortcut('postgresql')

        #Define our connection string
        conn_string = "host='localhost' dbname='postgres' user='postgres' password=''"
        conn_string += " port='%d'" % configuration.g_config_dict['POSTGRESQL_PORT']

        # print the connection string we will use to connect
        print "Connecting to database\n	->%s" % (conn_string)

        #Check if postgresql started correctly
        retry_cnt = 0
        while True:
            try:
                # get a connection, if a connect cannot be made an exception will be raised here
                conn = psycopg2.connect(conn_string)
                break
            except psycopg2.OperationalError:
                retry_cnt += 1
                print "retrying to connect postgresql server"
                if retry_cnt > 80:
                    print "postgresql start failed"
                    break


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
    #Other initial apps need to be launched may be added to initial_launcher
    #print 'POSTGRESQL_PORT:', os.environ.get("POSTGRESQL_PORT")
    #start_app_shortcut("start_ext")
    sys.stdout.flush()
    #wait_for_app(["start_ext"])
    #wait_for_app(["runserver"])
    #start_app_shortcut("tagging")
    #The following is not working as tube logging service is not started automatically currently
    #start_app_shortcut("tube_logging_service", ["--input", "ufs_test_tube"])

    
    
    
    