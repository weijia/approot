from libs.utils.filetools import get_free_timestamp_filename_in_path
import libsys
from libs.utils.misc import ensure_dir
import libs.utils.transform as transform
from libs.compress.enc_7z import EncZipFileOn7Zip

from libs.logSys.logSys import *

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
    def __init__(self, trunk_data_path=gWorkingDir, package_class=EncZipFileOn7Zip, ext=".7z", password='123'):
        super(CompressedStorage, self).__init__()
        self.trunk_data_path = trunk_data_path
        ensure_dir(self.trunk_data_path)
        ####################
        # The following var is not expected to be used in outside of this class
        self.package_class = package_class
        self.password = password
        self.ext = ext
        self.package_file = None
        self.package_file_full_path = None

    def add_file(self, full_path):
        compress_size = self.get_current_archive_file().addfile(unicode(full_path), unicode(full_path))
        return compress_size

    def finalize_one_trunk(self):
        self.package_file.close()
        #Set attribute so new zip will be created if this object is still in use
        self.package_file = None
        return self.package_file_full_path

    def get_storage_id(self):
        return "zip_file_storage://" + transform.format_path(self.trunk_data_path)

    ################################################
    # The following functions are not recommended to be called from outside of this class
    def get_current_archive_file(self):
        if self.package_file is None:
            self.package_file_full_path = transform.format_path(
                get_free_timestamp_filename_in_path(self.trunk_data_path, self.ext))
            self.package_file = self.package_class(self.package_file_full_path, 'w', self.password)
        return self.package_file