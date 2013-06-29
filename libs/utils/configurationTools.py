import encodingTools
import os
#commaEncoding = "gbk"
import libsys
import sys
#print sys.path
#import libs.utils.simplejson as json
'''
def getTagSeparator():
    #"\xa3\xac" is a "," in GBK
    return u","+"\xa3\xac".decode(commaEncoding)
'''
def getFsProtocolSeparator():
    #Replace : with _ and replace _ with __
    return "://"
    
def getLocalHostId():
    return "q19420-01"
    
def getRootDir():
    #return 'd:/tmp/fileman/'
    return libsys.get_root_dir()

'''
class configuration:
    def __init__(self, dbSysInst):
        self.db = dbSysInst.getDb("configuration")
    def __getitem__(self, key):
        print self.db[key]
        return self.db[key][0]
    def __setitem__(self, key, value):
        del self.db[key]
        self.db[key] = value
        print self.db[key]
    def has_key(self, key):
        try:
            a = self.db[key]
            print a
            return True
        except KeyError:
            return False
    def __delitem__(self, key):
        del self.db[key]
'''
class configuration:
    def __init__(self):
        try:
            sf = open(os.path.join(getRootDir(), 'config.json'), 'r')
            self.db = json.load(sf)
        except IOError:
            self.db = {}

    def __getitem__(self, key):
        print self.db[key]
        return self.db[key]
        
    def __setitem__(self, key, value):
        try:
            del self.db[key]
        except KeyError:
            pass
        self.db[key] = value
        s = json.dumps(self.db, sort_keys=True, indent=4)
        #s = json.dumps(self.db)
        f = open(os.path.join(getRootDir(), 'config.json'), 'w')
        f.write(s)
        f.close()

        print self.db[key]
    def has_key(self, key):
        return self.db.has_key(key)
        
    def __delitem__(self, key):
        del self.db[key]
        
    def get(self, key, default = None):
        if not self.db.has_key(key):
            self.__setitem__(key, default)
        return self.db[key]


if __name__ == '__main__':
    print getTagSeparator()
    