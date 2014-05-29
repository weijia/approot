import logging
import zipfile
from libtool import include_sub_folder_in_root_path, include, find_root
include_sub_folder_in_root_path(__file__, "approot", "libs")
include(find_root("approot"))
import configuration
from extra_settings.init_settings import init_settings
__inited_setting = init_settings()