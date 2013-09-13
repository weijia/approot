import os
import cbsettings
from django.conf import settings
import importlib

settings_class_str = 'rootapp.separated_setting_classes.with_ui_framework.WithUiFramework'

os.environ.setdefault('DJANGO_SETTINGS_FACTORY', settings_class_str)
cbsettings.configure()


def get_settings_module_name():
    print settings_class_str.rsplit('.', 1)[0]
    return settings_class_str.rsplit('.', 1)[0]


def get_settings_class_name():
    print settings_class_str.rsplit('.', 1)[1]
    return settings_class_str.rsplit('.', 1)[1]


def get_settings():
    return getattr(importlib.import_module(get_settings_module_name()), get_settings_class_name()).__class__


def initialize_settings():

    settings_module = get_settings()
    app_settings = {}

    for attr in dir(settings_module):
        if attr == attr.upper():
            print attr, ":", getattr(settings_module, attr)
            app_settings[attr] = getattr(settings_module, attr)
    settings.configure(**app_settings)
