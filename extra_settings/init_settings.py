import os
from libtool import include_file_sibling_folder, include_in_folder, find_root_path, get_parent_folder
include_in_folder(get_parent_folder(__file__), "libs")

from djangoautoconf import DjangoAutoConf
# configuration should not be imported here as setup.py will use this file,
# but will need some different database settings
#import configuration


def init_settings():
    include_file_sibling_folder(__file__, "keys")
    c = DjangoAutoConf()
    c.set_default_settings("rootapp.settings")
    root_folder = find_root_path(__file__, 'approot')
    c.set_root_dir(root_folder)
    c.set_key_dir(os.path.join(root_folder, "keys"))
    c.add_extra_settings(["extra_settings.settings",
                          #"local_postgresql_settings",
                          "extra_settings.build_settings"])
    c.configure(['guardian', 'pagination', 'django_social_auth', 'django_registration'])
    return c
