#!/usr/bin/env python
import os
import sys
from djangoautoconf import DjangoAutoConf
from libs.utils.console import unbuffer_console
from libs.utils.folder import get_folder
from libs.utils.syspath import include_file_sibling_folder

pwd = os.getcwd()
include_file_sibling_folder(__file__, "libs")
include_file_sibling_folder(__file__, "ui_framework")


unbuffer_console()


if __name__ == "__main__":
    #import rootapp.ufs_django_settings

    #Added keys folder to path so DjangoAutoConf can find keys in it
    include_file_sibling_folder(__file__, "keys")
    c = DjangoAutoConf()
    c.set_default_settings("ufs.settings")
    c.set_root_dir(get_folder(__file__))
    c.add_extra_settings(["extra_settings.settings"])
    c.configure(['guardian'])

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
