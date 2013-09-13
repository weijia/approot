from cbsettings import DjangoDefaults
import customized_settings

class RootSettings(DjangoDefaults):
    pass
    
i = RootSettings()

for attr_name in dir(customized_settings):
    if attr_name == attr_name.upper():
        setattr(i.__class__, attr_name, getattr(customized_settings, attr_name))