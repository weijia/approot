#from cbsettings import DjangoDefaults
from rootapp.cbsettings_root import RootSettings


class Emtpy(RootSettings):
    INSTALLED_APPS = RootSettings.INSTALLED_APPS
