##################################
# Added for BAE
##################################
try:
    from bae.core import const
    import bae_secrets

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': bae_secrets.database_name,
            'USER': const.MYSQL_USER,
            'PASSWORD': const.MYSQL_PASS,
            'HOST': const.MYSQL_HOST,
            'PORT': const.MYSQL_PORT,
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    ##################################
except:
    pass

#############
# You must enable memcache in BAE before enable the following
try:
    from bae.core import const
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': const.CACHE_ADDR,
            'TIMEOUT': 60,
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
except:
    pass


EMAIL_BACKEND = 'django.core.mail.backends.bcms.EmailBackend'

try:
    from bae.core import const
    from objsys.baidu_mail import EmailBackend

    EMAIL_BACKEND = 'objsys.baidu_mail.EmailBackend'
except:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


#EMAIL_BACKEND = 'django.core.mail.backends.bcms.EmailBackend'
#EMAIL_BCMS_QNAME = 'fe417333f4c4f34d6e0d07c76f179ba1'