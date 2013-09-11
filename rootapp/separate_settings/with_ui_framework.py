import sys
#print sys.modules
#print globals()
globals().update(vars(sys.modules['rootapp.customized_settings']))
try:
    INSTALLED_APPS += (
        'ui_framework',
    )
except:
    import traceback
    traceback.print_exc()