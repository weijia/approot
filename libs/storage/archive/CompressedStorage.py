#import re
import localLibSys
#import wwjufsdatabase.libs.utils.simplejson as json
import wwjufsdatabase.libs.utils.transform as transform
#import localLibs.objSys.ufsObj as ufsObj
import wwjufsdatabase.libs.utils.fileTools as fileTools
import localLibs.utils.misc as misc
from localLibs.compress.EncZipFileOn7Zip import EncZipFileOn7Zip


from localLibs.logSys.logSys import *

gWorkingDir = "d:/tmp/working/zipfilestorage"

class StorageInterface(object):
    def __init__(self):
        pass
    
    def add_file(self, itemObj):
        pass
    
    def finalize_one_trunk(self):
        pass
    def get_storage_id(self):
        '''
        Used to identify this storage
        '''
        pass

    
class CompressedStorage(object):
    def __init__(self, trunk_data_path = gWorkingDir, package_class = EncZipFileOn7Zip, ext = ".7z", passwd = '123'):
        super(CompressedStorage, self).__init__()
        self.trunk_data_path = trunk_data_path
        misc.ensureDir(self.trunk_data_path)
        ####################
        # The following var is not expected to be used in outside of this class
        self.package_class = package_class
        self.passwd = passwd
        self.ext = ext
        self.package_file = None
        self.package_file_full_path = None
            
    def add_file(self, full_path):
        compress_size = self.getZipFile().addfile(unicode(full_path), unicode(full_path))
        return compress_size

    def finalize_one_trunk(self):
        self.package_file.close()
        #Set attribute so new zip will be created if this object is still in use
        self.package_file = None
        return self.package_file_full_path
    def get_storage_id(self):
        return "zip_file_storage://"+transform.transformDirToInternal(self.trunk_data_path)
    
    ################################################
    # The following functions are not recommended to be called from outside of this class
    def getZipFile(self):
        if self.package_file is None:
            self.package_file_full_path = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.trunk_data_path, self.ext))
            self.package_file = self.package_class(self.package_file_full_path, 'w', self.passwd)
        return self.package_file
    