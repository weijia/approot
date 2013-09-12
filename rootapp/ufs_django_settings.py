import os
import cbsettings
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_FACTORY', 'rootapp.separated_setting_classes.with_ui_framework.WithUiFramework')
cbsettings.configure()
#import sys
#print sys.modules


def initialize_settings():
    # Well this isn't quite as clean as I'd like so
    # feel free to suggest something more appropriate
    #from rootapp.settings import *
    #app_settings = locals().copy()
    #del app_settings['self']
    #The following line just set the environment string
    #import rootapp.ufs_django_settings
    '''
    print os.environ["DJANGO_SETTINGS_MODULE"]
    settings_module = getattr(__import__(os.environ["DJANGO_SETTINGS_MODULE"]),
                              os.environ["DJANGO_SETTINGS_MODULE"].rsplit(".", 1)[1])
    '''
    from rootapp.separated_setting_classes.with_ui_framework import WithUiFramework
    s = WithUiFramework()
    settings_module = s.__class__
    app_settings = {}
    #print '------------------------------------'
    #print dir(settings_module)
    #print getattr(settings_module, os.environ["DJANGO_SETTINGS_MODULE"].split('.')[1])
    #print dir(getattr(settings_module, os.environ["DJANGO_SETTINGS_MODULE"].split('.')[1]))
    for attr in dir(settings_module):
        if attr == attr.upper():
            print attr, ":", getattr(settings_module, attr)
            app_settings[attr] = getattr(settings_module, attr)
    settings.configure(**app_settings)
