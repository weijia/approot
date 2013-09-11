import sys
#print sys.modules
#print globals()
try:
    globals().update(vars(sys.modules['rootapp.customized_settings']))
    INSTALLED_APPS += (
        #'desktop.filemanager',
        'ui_framework',
        'ui_framework.collection_management',
        'guardian',
        'tags',
        'ui_framework.connection',
        'ui_framework.normal_admin',
        'win_smb',
        'thumbapp',
    )
except:
    import traceback
    traceback.print_exc()