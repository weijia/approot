#from separated_setting_classes.with_ui_framework import WithUiFramework
from cbsettings import DjangoDefaults


class RootSettings(DjangoDefaults):
    pass


s = RootSettings()

import customized_settings

for attr in dir(customized_settings):
    if attr != attr.upper():
        continue
    setattr(s.__class__, attr, getattr(customized_settings, attr))