##################################
# Added for BAE
##################################


try:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': const.CACHE_ADDR,
            'TIMEOUT': 60,
        }
    }
except:
    pass
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
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    ###Or
    #SESSION_ENGINE = 'django.contrib.sessions.backends.db'
    ##################################
except:
    pass
    
EMAIL_BACKEND = 'django.core.mail.backends.bcms.EmailBackend'

try:
    from objsys.baidu_mail import EmailBackend
    EMAIL_BACKEND = 'objsys.baidu_mail.EmailBackend'
except:
    EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

