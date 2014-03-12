import psycopg2
from config import get_postsql_server_port
import libsys
from services.svc_base.ext_app_if import ExtAppMgrInterface
from services.svc_base.launcher_interface import Launcher
__author__ = 'Richard'


class PostgresApp(ExtAppMgrInterface):
    def __init__(self):
        ###########################
        # Start postgresql
        ###########################
        Launcher.start_app_with_name_param_list_no_wait('postgresql')

        #Define our connection string
        conn_string = "host='localhost' dbname='postgres' user='postgres' password=''"
        conn_string += " port='%d'" % get_postsql_server_port()

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