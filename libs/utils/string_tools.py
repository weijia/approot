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
    cl("input:", unicode_str, "output:", res)
    return res


def unquote_unicode(quoted_str):
    #cl(urllib2.unquote(quoted_str))
    cl("input:", quoted_str)
    result = urllib2.unquote(quoted_str).decode('utf8')
    cl("output:", result)
    return result

