from libtool import include_sub_folder_in_root_path
include_sub_folder_in_root_path(__file__, "approot", "libs")
from extra_settings.init_settings import init_settings
import configuration
init_settings()

