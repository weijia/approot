#!/usr/bin/env python
# -*- coding: utf-8 -*-
import importlib
import os
import sys
import base_settings
from utils import dump_attrs


class RootDirNotExist(Exception):
    pass


class KeyDirNotExist(Exception):
    pass


class DjangoAutoConf(object):
    def __init__(self, default_settings_import_str=None, root_dir=None, key_dir=None):
        self.default_settings_import_str = default_settings_import_str
        self.root_dir = root_dir
        #Default keys is located at ../keys relative to universal_settings module?
        self.key_dir = key_dir
        self.extra_settings = []

    def set_default_settings(self, default_settings_import_str):
        self.default_settings_import_str = default_settings_import_str

    def set_root_dir(self, root_dir):
        self.root_dir = root_dir
        self.key_dir = os.path.abspath(os.path.join(root_dir, "keys"))

    def set_key_dir(self, key_dir):
        self.key_dir = key_dir

    def add_extra_settings(self, extra_setting_list):
        self.extra_settings.extend(extra_setting_list)

    def check_params(self):
        if not os.path.exists(self.root_dir):
            raise RootDirNotExist
        if not os.path.exists(self.key_dir):
            #logging.getLogger().error("key dir not exist: "+self.key_dir)
            print "key dir not exist: "+self.key_dir
            raise KeyDirNotExist

    def configure(self, features=[]):
        self.check_params()

        #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoautoconf.base_settings")
        os.environ["DJANGO_SETTINGS_MODULE"] = "djangoautoconf.base_settings"

        ordered_import_list = [self.default_settings_import_str,
                               "djangoautoconf.sqlite_database"
                               #"djangoautoconf.mysql_database"
                                ]

        ordered_import_list.extend(self.extra_settings)
        for one_setting in ordered_import_list:
            self.import_based_on_base_settings(one_setting)

        for feature in features:
            self.import_based_on_base_settings("djangoautoconf.features."+feature)

        secret_key = get_or_create_secret_key(self.key_dir)
        PROJECT_PATH = os.path.abspath(os.path.abspath(self.root_dir))
        setattr(base_settings, "SECRET_KEY", secret_key)
        setattr(base_settings, "PROJECT_PATH", PROJECT_PATH)
        setattr(base_settings, "STATIC_ROOT", os.path.abspath(os.path.join(PROJECT_PATH, 'static')))
        #dump_attrs(base_settings)

    def get_settings(self):
           return base_settings

    def import_based_on_base_settings(self, module_import_path):
        #######
        # Inject attributes to builtin and import all other modules
        # Ref: http://stackoverflow.com/questions/11813287/insert-variable-into-global-namespace-from-within-a-function
        self.init_builtin()
        self.inject_attr()
        new_base_settings = importlib.import_module(module_import_path)
        self.remove_attr()
        update_base_settings(new_base_settings)

    def inject_attr(self):
        for attr in dir(base_settings):
            if attr != attr.upper():
                continue
            value = getattr(base_settings, attr)
            if hasattr(self.builtin, attr):
                raise "Attribute already exists"
            self.builtin[attr] = value

    def remove_attr(self):
        for attr in dir(base_settings):
            if attr != attr.upper():
                continue
            value = getattr(base_settings, attr)
            del self.builtin[attr]

    def init_builtin(self):
        try:
            self.__dict__['builtin'] = sys.modules['__builtin__'].__dict__
        except KeyError:
            self.__dict__['builtin'] = sys.modules['builtins'].__dict__


def update_base_settings(new_base_settings):
    for attr in dir(new_base_settings):
        if attr != attr.upper():
            continue
        value = getattr(new_base_settings, attr)
        setattr(base_settings, attr, value)


def get_or_create_secret_key(key_folder_path):
    #######################
    # Set secret key
    try:
        if not (key_folder_path in sys.path):
            sys.path.append(key_folder_path)
            from secret_key import SECRET_KEY
            sys.path.remove(key_folder_path)
        else:
            from secret_key import SECRET_KEY
    except ImportError:
        try:
            from django.utils.crypto import get_random_string
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            secret_key = get_random_string(50, chars)

            secret_file = open(os.path.join(key_folder_path, 'secret_key.py'), 'w')
            secret_file.write("SECRET_KEY='%s'" % secret_key)
            secret_file.close()
            from secret_key import SECRET_KEY
        except Exception:
            import traceback
            traceback.print_exc()
            #In case the above not work, use the following.
            # Make this unique, and don't share it with anybody.
            SECRET_KEY = 'd&amp;x%x+^l@qfxm^2o9x)6ct5*cftlcu8xps9b7l3c$ul*n&amp;%p-k'
    return SECRET_KEY