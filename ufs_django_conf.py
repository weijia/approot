from libtool import include_sub_folder_in_root_path
include_sub_folder_in_root_path(__file__, "approot", "libs")
import configuration
from extra_settings.init_settings import init_settings
__inited_setting = init_settings()