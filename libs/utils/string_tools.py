
    
    
class SpecialEncoder(object):
    def encode(self, unicode_str):
        if unicode != type(unicode_str):
            raise 'Only support unicode string'
        return unicode_str.replace(u"\\", u"\\\\").replace(u"&", u"\\x%02x"%ord('&')).replace("?", "\\x%02x"%ord('?'))
        
    def decode(self, unicode_str):
        if unicode != type(unicode_str):
            raise 'Only support unicode string'
        return unicode_str.replace(u"\\x%02x"%ord('&'), u"&").replace("\\x%02x"%ord('?'), u'?').replace(u"\\", u"\\\\")
