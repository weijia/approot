#coding:utf8
#author:richardwangwang@gmail.com  https://github.com/weijia
#Modified from weibo.py
"""
Baidu OAuth2 support.

This script adds support for Baidu OAuth service. An application must
be registered first on http://developer.baidu.com/

BAIDU_CLIENT_KEY and BAIDU_CLIENT_SECRET must be defined in the settings.py
correctly.

#By default account id,profile_image_url,gender are stored in extra_data field,
#check OAuthBackend class for details on how to extend it.
"""
from urllib import urlencode

from django.utils import simplejson

from social_auth.backends import OAuthBackend, BaseOAuth2
from social_auth.utils import dsa_urlopen


BAIDU_SERVER = 'openapi.baidu.com'
BAIDU_REQUEST_TOKEN_URL = 'https://%s/oauth/2.0/token' % BAIDU_SERVER
BAIDU_ACCESS_TOKEN_URL = 'https://%s/oauth/2.0/token' % BAIDU_SERVER
BAIDU_AUTHORIZATION_URL = 'https://%s/oauth/2.0/authorize' % BAIDU_SERVER


class BaiduBackend(OAuthBackend):
    """Baidu OAuth authentication backend"""
    name = 'baidu'
    '''
    # Default extra data to store
    EXTRA_DATA = [
        ('id', 'id'),
        ('name', 'username'),
        ('profile_image_url', 'profile_image_url'),
        ('gender', 'gender')
    ]
    '''

    def get_user_id(self, details, response):
        """
        This function will be called by social_auth/backends/__init__.py, this id will be kept in social auth
        """
        #return response['uid']
        return self.baidu_info["uid"]

    def get_user_details(self, response):
        """
        This function will be called by social_auth/backends/__init__.py, username and first name is a must
        """
        data = {'access_token': response['access_token']}
        url = 'https://openapi.baidu.com/rest/2.0/passport/users/getLoggedInUser?'+urlencode(data)
        #Result: {"uid":"123456","uname":"xxxxxx","portrait":"1234567800000000000"}
        try:
            result = dsa_urlopen(url).read()
            print result
            self.baidu_info = simplejson.loads(result)
            return {"username": self.baidu_info["uname"]}
        except (ValueError, KeyError, IOError):
            return None



class BaiduAuth(BaseOAuth2):
    """Weibo OAuth authentication mechanism"""
    AUTHORIZATION_URL = BAIDU_AUTHORIZATION_URL
    REQUEST_TOKEN_URL = BAIDU_REQUEST_TOKEN_URL
    ACCESS_TOKEN_URL = BAIDU_ACCESS_TOKEN_URL
    AUTH_BACKEND = BaiduBackend
    SETTINGS_KEY_NAME = 'BAIDU_CLIENT_KEY'
    SETTINGS_SECRET_NAME = 'BAIDU_CLIENT_SECRET'
    REDIRECT_STATE = False

    def user_data(self, access_token, *args, **kwargs):
        uid = kwargs.get('response', {}).get('uid')
        data = {'access_token': access_token, 'uid': uid}
        url = 'https://pcs.baidu.com/rest/2.0/pcs/quota'
        try:
            result = dsa_urlopen(url).read()
            print result
            return simplejson.loads(result)
        except (ValueError, KeyError, IOError):
            return None


# Backend definition
BACKENDS = {
    'baidu': BaiduAuth
}
