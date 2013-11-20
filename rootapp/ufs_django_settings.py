import os
import cbsettings
from libs.django_settings_overrider.django_for_cherrypy import get_settings

django_cb_class_full_name = 'rootapp.separated_setting_classes.with_ui_framework.WithUiFramework'

os.environ.setdefault('DJANGO_SETTINGS_FACTORY', django_cb_class_full_name)
cbsettings.configure()


def get_ufs_settings():
    return get_settings(django_cb_class_full_name)