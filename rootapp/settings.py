# Django settings for rootapp project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
######### Added for relative path start
import os
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
RUNNING_PATH = os.path.abspath(os.getcwd())
########## Added for relative path end


################Start of login
#Added for login redirect
LOGIN_REDIRECT_URL = "/objsys/manager/"
#If need a url name for default redirect, use the following setting instead of the above one. allauth will reverse the following name to url.
#LOGIN_REDIRECT_URLNAME

################End of login


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS
from os import environ
postgresql = environ.get("POSTGRESQL_ROOT", "")
postgresql_port = environ.get("POSTGRESQL_PORT", "")
if postgresql:
    #Local database
    '''
    MYSQL_DB = 'mysite' 
    MYSQL_USER = 'root' 
    MYSQL_PASS = '' 
    MYSQL_HOST_M = '127.0.0.1' 
    MYSQL_HOST_S = '127.0.0.1' 
    MYSQL_PORT = '3306' 
    '''
    print 'using postgresql', postgresql, postgresql_port
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'postgres',                      # Or path to database file if using sqlite3.
            'USER': 'postgres',                      # Not used with sqlite3.
            'PASSWORD': '',                  # Not used with sqlite3.
            'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
            'PORT': str(postgresql_port),                      # Set to empty string for default. Not used with sqlite3.
        }
    }
else:

    debug = not environ.get("APP_NAME", "") 
    if debug:
        #Local database
        '''
        MYSQL_DB = 'mysite' 
        MYSQL_USER = 'root' 
        MYSQL_PASS = '' 
        MYSQL_HOST_M = '127.0.0.1' 
        MYSQL_HOST_S = '127.0.0.1' 
        MYSQL_PORT = '3306' 
        '''
        print 'using sqlite3'
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
        
    else: 
    #SAE
        import sae.const 
        MYSQL_DB = sae.const.MYSQL_DB 
        MYSQL_USER = sae.const.MYSQL_USER 
        MYSQL_PASS = sae.const.MYSQL_PASS 
        MYSQL_HOST_M = sae.const.MYSQL_HOST 
        MYSQL_HOST_S = sae.const.MYSQL_HOST_S 
        MYSQL_PORT = sae.const.MYSQL_PORT
        
        DATABASES = { 
            'default': { 
                'ENGINE': 'django.db.backends.mysql', 
                'NAME': MYSQL_DB, 
                'USER': MYSQL_USER, 
                'PASSWORD': MYSQL_PASS, 
                'HOST': MYSQL_HOST_M, 
                'PORT': MYSQL_PORT, 
            } 
        }



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, '../static')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
#SECRET_KEY = 'g-yjv2wm_=_+r2j9v2u3ak$!b+i2qz=#e2#h3nmrt2l6+_wps$'
try:
    from secret_key import *
except ImportError:
    from django.utils.crypto import get_random_string
    import os
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(50, chars)
    SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))

    secret_file = open(os.path.join(SETTINGS_DIR, 'secret_key.py'), 'w')
    secret_file.write("SECRET_KEY='%s'" % secret_key)
    secret_file.close()
    from secret_key import *


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)
#################################
# Added for auth
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.request",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    "django.core.context_processors.static",
    'ui_framework.objsys.custom_context_processors.head_form',
    'django.core.context_processors.request',
)
ANONYMOUS_USER_ID = -1

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    'guardian.backends.ObjectPermissionBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'pagination.middleware.PaginationMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rootapp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'rootapp.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(RUNNING_PATH, 'templates'),   # The comma is a must as otherwise, it will not be treated as a set?
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'tagging',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    #'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.github',
    #'allauth.socialaccount.providers.linkedin',
    #'allauth.socialaccount.providers.openid',
    #'allauth.socialaccount.providers.soundcloud',
    #'allauth.socialaccount.providers.twitter',
    'desktop.filemanager',
    'ui_framework',
    'ui_framework.objsys',
    'ui_framework.collection_management',
    'guardian',
    'tags',
    'ui_framework.connection',
    'ui_framework.normal_admin',
    'win_smb',
    'object_filter',
    'thumbapp',
    #'pagination',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


#Added for app config
import os
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
'''
for app in INSTALLED_APPS:
    local_settings = os.path.join(PROJECT_DIR, app, 'local_settings.py')
    if os.path.isfile(local_settings):
        execfile(local_settings)
'''
execfile(os.path.join(PROJECT_DIR, "local_settings.py"))

from local_keys import *