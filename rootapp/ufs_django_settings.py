import os
import cbsettings
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_FACTORY', 'rootapp.separated_setting_classes.with_ui_framework.WithUiFramework')
cbsettings.configure()


def get_settings():
    from rootapp.separated_setting_classes.with_ui_framework import WithUiFramework
    return WithUiFramework.__class__


def initialize_settings():

    settings_module = get_settings()
    app_settings = {}

    for attr in dir(settings_module):
        if attr == attr.upper():
            print attr, ":", getattr(settings_module, attr)
            app_settings[attr] = getattr(settings_module, attr)
    settings.configure(**app_settings)
