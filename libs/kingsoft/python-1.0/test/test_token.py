#coding:utf-8
#author: leanse

import sys
sys.path.append("..")

import session
import client
import time

def testRequestToken():
    sess = session.KuaipanSession("", "", "app_folder")
    api = client.KuaipanAPI(sess)
    print api.requestToken(callback = None)
    time.sleep(30)
    print api.accessToken()

if __name__ == "__main__":
    testRequestToken()    
