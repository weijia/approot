from stat import *
import md5
import libsys
import os

#######
# TODO: to support other platform such as Linux?
os.environ["PATH"] = os.environ["PATH"]+";"+os.path.join(libsys.get_root_dir(), 'libs')
import magic

gHeadMd5Length = 1024


class LocalObj(object):
    def __init__(self, full_path):
        if not os.path.exists(full_path):
            raise IOError
        self.full_path = full_path

    def get_header_md5(self):
        try:
            f = open(self.full_path, 'rb')
        except IOError:
            #print "can not read", fullPath
            raise IOError
            return 0

        data = f.read(gHeadMd5Length)
        '''
        p = "d:/tmp/a.xls"
        while os.path.exists(p):
            p = p+"t"
        wf = open(p, 'wb')
        wf.write(data)
        wf.close()
        '''
        res = unicode(md5.new(data).hexdigest())
        f.close()
        return res
            
    def get_size(self):
        return os.stat(self.full_path)[ST_SIZE]
        
    def get_type(self):
        root_path = libsys.get_root_dir()
        magic_path = os.path.join(root_path, "share\\misc\\magic")
        #print magic_path
        #print 'magic path: ',magic_path
        if not os.path.exists(magic_path):
            raise "Magic file lost"
        #print "magic path is", magic_path
        #os.environ["MAGIC"] = magic_path
        m = magic.Magic(magic_file=magic_path)
        #print type(fullPath)
        #print 'utf8, 3', fullPath.encode('utf8')
        #print 'exists?', os.path.exists(fullPath)
        #print 'exists?', os.path.exists(fullPath.encode('gbk'))
        #print 'exists?', os.path.exists(fullPath.encode('utf8'))
        try:
            res = m.from_file(self.full_path)
        except:
            import traceback
            traceback.print_exc()
            return 'unknown type according to magic'
        return res