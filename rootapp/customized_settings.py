from settings import *
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'data.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(PROJECT_PATH, '../static')

try:
    from secret_key import *
except ImportError:
    try:
        from django.utils.crypto import get_random_string
        import os
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = get_random_string(50, chars)
        SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))

        secret_file = open(os.path.join(SETTINGS_DIR, 'secret_key.py'), 'w')
        secret_file.write("SECRET_KEY='%s'" % secret_key)
        secret_file.close()
        from secret_key import *
    except:
        #In case the above not work, use the following.
        # Make this unique, and don't share it with anybody.
        SECRET_KEY = 'd&amp;x%x+^l@qfxm^2o9x)6ct5*cftlcu8xps9b7l3c$ul*n&amp;%p-k'
        
    
ANONYMOUS_USER_ID = -1
    
MIDDLEWARE_CLASSES += (
    #'libs.objsys.middleware.XsSharingMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

INSTALLED_APPS += (
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'guardian',
    'social_auth',
    'socialprofile',
    #'smuggler',
    'registration',
    'registration_defaults',
    'pagination',
    'objsys',
    'object_filter',
    'webmanage',
    'tagging',
    'south',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
)

#Added for app config
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from local_settings import *
except:
    print "No local_settings"
    pass
try:
    from local_keys import *
except ImportError:
    print "No local_keys"
    pass
    
'''
for app in INSTALLED_APPS:
    local_settings = os.path.join(PROJECT_DIR, app, 'local_settings.py')
    if os.path.isfile(local_settings):
        execfile(local_settings)
'''

# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone. Following is the default in settings.py
#TIME_ZONE = 'America/Chicago'

print "start importing"

setting_module_name_list = []

modules_in_folder = []
try:
    for filename in os.listdir(os.path.join(PROJECT_DIR, 'separate_settings')):
        if 0 == filename.find('__init__'):
            continue
        if -1 != filename.find(".pyc"):
            continue
        modules_in_folder.append(filename.replace(".py", ""))
except:
    #In case listdir is not permitted (in BAE or SAE)
    pass

setting_module_name_list += modules_in_folder
import sys
sys.path.append(PROJECT_DIR)
print setting_module_name_list
for setting_module_name in setting_module_name_list:
    settings_module = getattr(__import__("separate_settings."+setting_module_name), setting_module_name)
    #print "importing", "separate_settings."+setting_module_name #,dir(getattr(settings_module, setting_module_name))
    for attr in dir(settings_module):
        if attr[0:2] == "__":
            #Ignore built in attributes
            continue
        if attr != attr.upper():
            #Only import uppercase var
            continue
        #print attr, ": ", globals().get(attr, ""), getattr(settings_module, attr)
        try:
            globals()[attr] = getattr(settings_module, attr)
        except:
            import traceback
            traceback.print_exc()
        print attr, ": ", globals().get(attr, "")
