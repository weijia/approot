#!/usr/bin/env python
import sys
#from configuration import *
from extra_settings.init_settings import init_settings
from libtool import include_file_sibling_folder_ex
include_file_sibling_folder_ex("libs")


from ufs_utils.console import unbuffer_console

unbuffer_console()


if __name__ == "__main__":
    #import rootapp.ufs_django_settings

    #Added keys folder to path so DjangoAutoConf can find keys in it
    init_settings()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
