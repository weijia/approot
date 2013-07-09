#-*-coding:utf-8 -*-
'''
author:lixin
e-mail:lixin@lixin.me or li.lixin.vip@gmail.com
Create Date:2012-4-7
'''
import urllib 
import hmac
import hashlib
import base64
import time
import random
import urllib2
import json
import cookielib
import urlparse
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

import jinshan_key

########################################################################
class KuaiPan:
    """
    
Example:
    KuaiPan.consumer_key='your app key'
    KuaiPan.consumer_key_secret='your app key secret'

    kp=KuaiPan()
    tempToken=kp.requestToken()
    authLink=kp.authorize(tempToken["oauth_token"])
    print "please go to link:\n"+authLink
    aaa=raw_input("please input any key..")
    token=kp.accessToken()
    print kp.account_info()
    
    or
    
    kp=KuaiPan('token','token_secret')
    print kp.account_info()
    """
    consumer_key=jinshan_key.get_consumer_key() #your app key
    consumer_key_secret=jinshan_key.get_consumer_key_secret() #your app secret
    api_version="1"
    oauth_token=''
    oauth_token_secret=''
    #----------------------------------------------------------------------
    def __init__(self,oauth_token=None,oauth_token_secret=None):
        """Constructor"""
        if oauth_token:
            self.oauth_token=oauth_token
        if oauth_token_secret:
            self.oauth_token_secret=oauth_token_secret
        pass
    #----------------------------------------------------------------------
    def set_oauth(self,oauth_token=None,oauth_token_secret=None):
        """"""
        if oauth_token:
            self.oauth_token=oauth_token
        if oauth_token_secret:
            self.oauth_token_secret=oauth_token_secret
        pass        

    #----------------------------------------------------------------------
    def requestToken(self,oauth_callback=None):
        """"""
        url='https://openapi.kuaipan.cn/open/requestToken'
        args={}
        if oauth_callback:
            args["oauth_callback"]=oauth_callback
        link=self.signature(url,args)
        data= self._getResponse(link)
        self.oauth_token=data['oauth_token'].encode("utf8")
        self.oauth_token_secret=data['oauth_token_secret'].encode("utf8")
        return data
    #----------------------------------------------------------------------
    def authorize(self,oauth_token):
        """"""
        return 'https://www.kuaipan.cn/api.php?ac=open&op=authorise&oauth_token='+oauth_token
    #----------------------------------------------------------------------
    def accessToken(self,oauth_token=None):
        """"""
        url='https://openapi.kuaipan.cn/open/accessToken'
        args={}
        if oauth_token:
            args['oauth_token']=oauth_token
        link=self.signature(url,args)
        data= self._getResponse(link)
        self.oauth_token=data['oauth_token'].encode("utf8")
        self.oauth_token_secret=data['oauth_token_secret'].encode("utf8")
        return data 
        
        
    #----------------------------------------------------------------------
    def signature(self,baseUrl,kvs,httpMethod="GET"):
        """"""
        if not kvs.has_key('oauth_consumer_key') :
            kvs["oauth_consumer_key"]=self.consumer_key
        if not kvs.has_key('oauth_token') and len(self.oauth_token)>0:
            kvs["oauth_token"]=self.oauth_token
        if not kvs.has_key('oauth_signature_method'):
            kvs["oauth_signature_method"]="HMAC-SHA1"
        if not kvs.has_key("oauth_timestamp"):
            kvs["oauth_timestamp"]=str(int(time.time()))
        if not kvs.has_key('oauth_nonce'):
            kvs["oauth_nonce"]=str(int(time.time()))+str(random.randint(100,999)) #13
        if not kvs.has_key("oauth_version"):
            kvs['oauth_version']='1.0'
        queryString=[urllib.quote(k,safe='')+"="+urllib.quote(v,safe='') for k,v in kvs.items()]
        queryString.sort()
        baseStr="%s&%s&%s" % (httpMethod,urllib.quote(baseUrl,safe=""),
                                 urllib.quote("&".join(queryString),safe=""))
        ##
        myhmac=hmac.new(self.consumer_key_secret+"&"+self.oauth_token_secret,digestmod=hashlib.sha1)
        myhmac.update(baseStr)
        signatureValue=urllib.quote(base64.encodestring(myhmac.digest()).strip(),
                                    safe="")
        kvs["oauth_signature"]=signatureValue
        return "%s?%s" %(baseUrl,"&".join([k+"="+urllib.quote(v,safe=".-_~%") for k,v in kvs.items()]))
    #----------------------------------------------------------------------
    def _getResponse(self,url):
        """"""
        '''
        import os
        print os.environ["http_proxy"]
        #proxy = urllib2.ProxyHandler({'http': os.environ["http_proxy"], 'https': os.environ["http_proxy"]})
        #proxy = urllib2.ProxyHandler({'http': 'nsn-intra\\q19420:BErich34@10.159.192.62:8080', 'https': 'nsn-intra\\q19420:BErich34@10.159.192.62:8080'})

        #urllib2.urlopen('http://www.google.com')
        
        mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        mgr.add_password(None, 'https://openapi.kuaipan.cn', 'nsn-intra\\q19420', 'BErich34')        
        opener = urllib2.build_opener(urllib2.HTTPBasicAuthHandler(mgr),
            urllib2.HTTPDigestAuthHandler(mgr))
        req = opener.open(url)
        '''
        #proxy = urllib2.ProxyHandler({})
        #opener = urllib2.build_opener(proxy)
        #urllib2.install_opener(opener)
        # try:
            # req=urllib2.urlopen(url)
        # except IOError, e:
            # if hasattr(e, 'code'):
                # if e.code != 401:
                    # print 'We got another error'
                    # print e.code
                # else:
                    # print e.headers
                    # #print e.headers['www-authenticate']
        #req=urllib2.urlopen(url)
        
        import os
        #print os.environ["http_proxy"]
        proxy = urllib2.ProxyHandler({'http': os.environ["http_proxy"], 'https': os.environ["https_proxy"]})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        req=urllib2.urlopen(url)
        return json.loads(req.read())
        
    #----------------------------------------------------------------------
    def _getResponseWithCookie(self,url):
        """"""
        mycookie=cookielib.CookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(mycookie))
        req=opener.open(url)
        return req.read()
    #----------------------------------------------------------------------
    def _postFile(self,url,path):
        """"""
        register_openers()
        datagen, headers = multipart_encode({"file": open(path, "rb")})
        request = urllib2.Request( url, datagen, headers)
        data=json.loads(urllib2.urlopen(request).read() )
        return data 
    #----------------------------------------------------------------------
    def _url(self,url):
        """"""
        return url.replace("<v>",self.api_version)
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    #----------------------------------------------------------------------
    def metadata(self,path,root="app_folder",list=None,file_limit=None,page=None,page_size=None,filter_ext=None,sort_by=None ):
        """"""
        url=self._url("http://openapi.kuaipan.cn/<v>/metadata/"+root+"/")
        url=urlparse.urljoin(url,path)
        args={}
        if list:
            args["list"]=list
        if file_limit:
            args['file_limit']=file_limit
        if page:
            args["page"]=page
        if page_size:
            args["page_size"]=page_size
        if filter_ext:
            args['filter_ext']=filter_ext
        if sort_by:
            args['sort_by']=sort_by      
        link=self.signature(url,args)
        return self._getResponse(link)
        
    #----------------------------------------------------------------------
    def account_info(self):
        """"""
        url=self._url('http://openapi.kuaipan.cn/<v>/account_info')
        link=self.signature(url,{})
        data=self._getResponse(link)
        return data
    #----------------------------------------------------------------------
    def shares(self,path,root="app_folder"):
        """"""
        url=self._url("http://openapi.kuaipan.cn/<v>/shares/%s/%s" % (root,path ))
        link=self.signature(url,{})
        return self._getResponse(link)
    #----------------------------------------------------------------------
    def create_folder(self,path,root="app_folder"):
        """"""
        url=self._url("http://openapi.kuaipan.cn/<v>/fileops/create_folder")
        link=self.signature(url,{'path':path,'root':root})
        return self._getResponse(link)
    #----------------------------------------------------------------------
    def delete(self,path,root="app_folder",to_recycle="True"):
        """"""
        url=self._url("http://openapi.kuaipan.cn/<v>/fileops/delete")
        link=self.signature(url,{'path':path,'root':root,'to_recycle':to_recycle})
        return self._getResponse(link)
    #----------------------------------------------------------------------
    def move(self,from_path,to_path,root="app_folder"):
        """"""
        url=self._url('http://openapi.kuaipan.cn/<v>/fileops/move')
        link=self.signature(url,{'from_path':from_path,'to_path':to_path,'root':root })
        return self._getResponse(link)
    #----------------------------------------------------------------------
    def copy(self,from_path,to_path,root="app_folder"):
        """"""
        url=self._url('http://openapi.kuaipan.cn/<v>/fileops/copy')
        link=self.signature(url,{'from_path':from_path,'to_path':to_path,'root':root })
        return self._getResponse(link)
    #----------------------------------------------------------------------
    def upload(self,path,local_path,root="app_folder",overwrite="False",ip=None):
        """"""
        url=self._url('http://api-content.dfs.kuaipan.cn/<v>/fileops/upload_locate')
        args1={}
        if ip:
            args1["source_ip"]=ip 
        link=self.signature(url,args1)
        postUrl=self._getResponse(link)
        upload_url= postUrl['url'].rstrip('/')+'/1/fileops/upload_file'
        args2={'overwrite':overwrite,'root':root,'path':path}
        link2=self.signature(upload_url.encode('utf8'),args2,"POST")
        return self._postFile(link2,local_path)
    #----------------------------------------------------------------------
    def download(self,path,root="app_folder"):
        """"""
        url=self._url('http://api-content.dfs.kuaipan.cn/<v>/fileops/download_file')
        link=self.signature(url,{'path':path,'root':root})
        return self._getResponseWithCookie(link)
    #----------------------------------------------------------------------
    def thumbnail(self,path,width,height,root="app_folder"):
        """"""
        url=self._url('http://conv.kuaipan.cn/<v>/fileops/thumbnail')
        link=self.signature(url,{'path':path,'root':root,'width':width,'height':height})
        return self._getResponseWithCookie(link)
    #----------------------------------------------------------------------
    def documentView(self,path,docType,view='normal',has_zip="1",root='app_folder'):
        """
        docType=['pdf', 'doc', 'wps', 'csv', 'prn', 'xls', 'et', 'ppt', 'dps', 'txt', 'rtf']
        """
        url=self._url('http://conv.kuaipan.cn/<v>/fileops/documentView')
        link=self.signature(url,{'type':docType,'view':view,'zip':has_zip,'path':path,'root':root})
        return self._getResponseWithCookie(link)
    
        
            
            
if __name__=="__main__":
    print "start test..."
    kp=KuaiPan()
    tempToken=kp.requestToken()
    authLink=kp.authorize(tempToken["oauth_token"])
    print "please go to link:\n"+authLink
    aaa=raw_input("please input any key..")
    token=kp.accessToken()
    print 'oauth_token',token["oauth_token"]
    print 'oauth_token_secret',token['oauth_token_secret']
    print kp.account_info()
    #kp=KuaiPan('','')
    #print kp.metadata('')
    #kp.create_folder("autoCreate")
    #kp.delete("autoCreate")
    #kp.move('test3.jpg','wp-content/test3.jpg')
    #kp.copy('upload.jpg','upload2.jpg')
    #kp.upload('upload3.jpg',r'E:\picture\something\IMG0028B.jpg')
    #kp.upload('wp-content/test.txt',r'd:\test.txt')
    #data=kp.download('wp-content/test.txt')
    #open(r'd:\kuaipan-down.txt','wb').write(data)
    #data=kp.thumbnail('wp-content/test3.jpg','240','240')
    #open(r'd:\kkkkkk.jpg','wb').write(data)
    #data=kp.documentView('test.doc','doc')
    #open(r'd:\kkpppp.zip','wb').write(data)
    #
    
    