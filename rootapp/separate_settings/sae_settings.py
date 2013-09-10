import os
sae_app_name = os.environ.get("APP_NAME", "")
if sae_app_name != "":
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
