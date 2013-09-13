#from cbsettings import DjangoDefaults
from rootapp.cbsettings_root import RootSettings


class WithUiFramework(RootSettings):
    INSTALLED_APPS = RootSettings.INSTALLED_APPS + (
        #'desktop.filemanager',
        'ui_framework',
        'ui_framework.collection_management',
        'tags',
        'ui_framework.connection',
        'ui_framework.normal_admin',
        'win_smb',
        'thumbapp',
    )