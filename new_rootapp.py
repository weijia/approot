import os
from iconizer import Iconizer
from libs.utils.filetools import findAppInProduct
import configuration


def stop_postgresql():
    os.system(findAppInProduct("postgresql_stop"))


def main():
    try:
        i = Iconizer()
        i.add_close_listener(stop_postgresql)
        i.execute({"ext_svr": [findAppInProduct("new_ext_svr")]})
    except (KeyboardInterrupt, SystemExit):
        raise
    #print "stopping database"


if __name__ == '__main__':
    main()
    #os.system(findAppInProduct("postgresql_stop"))