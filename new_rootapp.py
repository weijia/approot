import os
from iconizer import Iconizer
from libs.utils.filetools import findAppInProduct


def main():
    Iconizer().execute({"ext_svr": [findAppInProduct("ext_svr")]})


if __name__ == '__main__':
    main()