#!/usr/bin/env python
import sys
from extra_settings.init_settings import init_settings
from libtool import include_file_sibling_folder
include_file_sibling_folder(__file__, "libs")

from utils.console import unbuffer_console

unbuffer_console()


if __name__ == "__main__":
    #import rootapp.ufs_django_settings

    #Added keys folder to path so DjangoAutoConf can find keys in it
    init_settings()

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
