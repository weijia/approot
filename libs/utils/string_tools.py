# -*- coding: utf8 -*-
import urllib2
from libs.logsys.logSys import *

class SpecialEncoder(object):
    def encode(self, unicode_str):
        if unicode != type(unicode_str):
            raise 'Only support unicode string'
        return unicode_str.replace(u"\\", u"\\\\").replace(u"&", u"\\x%02x"%ord('&')).replace("?", "\\x%02x"%ord('?'))
        
    def decode(self, unicode_str):
        if unicode != type(unicode_str):
            raise 'Only support unicode string'
        return unicode_str.replace(u"\\x%02x"%ord('&'), u"&").replace("\\x%02x"%ord('?'), u'?').replace(u"\\", u"\\\\")


def quote_unicode(unicode_str):
    if unicode != type(unicode_str):
        raise "Only support unicode string"
    res = urllib2.quote(unicode_str.encode('utf8'))
    #cl("input:", unicode_str, "output:", res)
    return res


def unquote_unicode(quoted_str):
    #cl(urllib2.unquote(quoted_str))
    #cl("input:", quoted_str)
    #We must encode the quoted_str to utf8 so urllib2.unquote will return utf8. Otherwise, it will return
    #unicode and unicode can not be decoded as utf8.
    if unicode == type(quoted_str):
        quoted_str = quoted_str.encode('utf8')
    result = urllib2.unquote(quoted_str)
    #cl(type(result))
    #cl(result.encode('gbk'))
    result = result.decode('utf8')
    #cl("output:", result)
    return result


if __name__ == "__main__":
    import os
    #encoded_str = quote_unicode(u"中文")
    #res = unquote_unicode('system_rest/%3Ffull_path%3DE%3A%5C%E5%BF%AB%E7%9B%98')
    res = unquote_unicode('local_filesystem%3A//E%3A%5C%E5%BF%AB%E7%9B%98')
    print type(res)
    #print os.path.exists(res.split('=')[1])
    print os.path.exists(res.split('//')[1])