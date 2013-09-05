import os
from iconizer import Iconizer
from libs.utils.filetools import findAppInProduct
import configuration


def main():
    try:
        Iconizer().execute({"ext_svr": [findAppInProduct("new_ext_svr")]})
    except (KeyboardInterrupt, SystemExit):
        raise

    #print "stopping database"
    os.system("D:\\codes\\python\\codes\\ufs_django\\approot\\libs\\services\\external_app\\postgresql_stop.bat")


if __name__ == '__main__':
    main()