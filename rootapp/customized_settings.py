import os

from settings import *


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
    'smuggler',
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

try:
    from static_settings_module_list import modules_in_folder
except:
    modules_in_folder = []
    try:
        for filename in os.listdir(os.path.join(PROJECT_DIR, 'separated_settings')):
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
    config_module = getattr(__import__("separated_settings."+setting_module_name), setting_module_name)
    #config_module = __import__("separated_settings."+setting_module_name, globals(), locals(), -1)

    # Load the config settings properties into the local scope.
    for setting in dir(config_module):
        if setting == setting.upper():
            #print setting, getattr(config_module, setting)
            locals()[setting] = getattr(config_module, setting)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    #'ui_framework.objsys.custom_context_processors.head_form',
    'django.core.context_processors.request',
)

# Import the configuration settings file - REPLACE projectname with your project
#print '--------------------------',DATABASES
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            #'handlers': ['mail_admins'],
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}