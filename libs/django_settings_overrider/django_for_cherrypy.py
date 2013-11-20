from django.conf import settings
import importlib


def get_module_name_from_str(importing_class_name):
    #print importing_class_name.rsplit('.', 1)[0]
    return importing_class_name.rsplit('.', 1)[0]


def get_class_name_from_str(importing_class_name):
    #print importing_class_name.rsplit('.', 1)[1]
    return importing_class_name.rsplit('.', 1)[1]


def get_settings(django_cb_class_full_name):
    settings_module = importlib.import_module(get_module_name_from_str(django_cb_class_full_name))
    #print settings_module
    #print getattr(settings_module, get_class_name_from_str(settings_class_str))
    return getattr(settings_module, get_class_name_from_str(django_cb_class_full_name))().__class__
    #return getattr(settings_module, get_settings_class_name()).__class__


def initialize_settings(django_cb_class_full_name):
    settings_module = get_settings(django_cb_class_full_name)
    print dir(settings_module)
    app_settings = {}

    for attr in dir(settings_module):
        if attr == attr.upper():
            print attr, ":", getattr(settings_module, attr)
            app_settings[attr] = getattr(settings_module, attr)
    settings.configure(**app_settings)
