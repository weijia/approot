BROKER_URL = 'django://'

INSTALLED_APPS += (
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    #'django.contrib.admindocs',
    #'desktop.filemanager',
    'objsys',
    'object_filter',
    'ui_framework',
    'ui_framework.collection_management',
    'tags',
    'ui_framework.connection',
    'ui_framework.normal_admin',
    'win_smb',
    'thumbapp',
    'guardian',
    'social_auth',
    'socialprofile',
    'smuggler',
    'registration',
    'registration_defaults',
    'pagination',
    'tagging',
    'south',
    'webmanage',
    'kombu.transport.django',
    'djcelery'
)

import logging
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
    logging.warning('using postgresql:'+postgresql+":"+postgresql_port)
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
    pass