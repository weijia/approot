import os.path
import os

import subprocess
from libs.app_framework.folders import get_app_full_path_by_name, get_or_create_app_data_folder
from libs.obj_related import test_keys
from libs.utils.misc import ensure_dir
from libs.utils.transform import format_path

CREATE_NO_WINDOW = 0x8000000

gLocalEncode = 'gbk'


def encode2local(s):
    if type(s) == unicode:
        return s.encode(gLocalEncode)
    else:
        return s


def decode2local(s):
    return s.decode(gLocalEncode)


#Every app will be start in the root dir of the source code (prodRoot)
#app = "..\\otherBin\\7za920\\7za.exe"


class DecZipFileOn7Zip(object):
    def __init__(self, file_path, mode="r", password='123'):
        self.file_path = file_path
        self.password = unicode(password)

    def extract_file(self, extracting_file, output_folder):
        if os.path.exists(self.file_path):
            original_size = os.stat(self.file_path).st_size
        else:
            original_size = 0
        cmd = (
            u'%s -p%s x "%s" "%s" -o%s' % (get_app_full_path_by_name("7z"), self.password, self.file_path,
                                      extracting_file, output_folder)).encode(gLocalEncode)
        print "command:", cmd
        print "current dir:", os.getcwd()
        process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
        #wait is used to wait for the child process to complete
        process.wait()
        print process.stdout.read()
        print process.stderr.read()
        return True

    def list(self):
        if os.path.exists(self.file_path):
            original_size = os.stat(self.file_path).st_size
        else:
            original_size = 0
        cmd = (u'%s -p%s l "%s"' % (get_app_full_path_by_name("7z"), self.password,
                                    self.file_path)).encode(gLocalEncode)
        print "command:", cmd
        print "current dir:", os.getcwd()
        process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, creationflags=CREATE_NO_WINDOW)
        #wait is used to wait for the child process to complete
        process.wait()
        #increased_size = os.stat(self.file_path).st_size - original_size
        lines = process.stdout.readlines()
        is_file_list_start = False
        file_info_line_list = []
        for line in lines:
            line = line.replace("\n","").replace("\r","")
            if '--------' in line:
                is_file_list_start = not is_file_list_start
                continue
            if is_file_list_start:
                #print line
                file_info_line_list.append(line)

        filename_list = []
        for file_info in file_info_line_list:
            filename_list.append(file_info.split(" ")[-1])

        return filename_list

    def close(self):
        pass


class FolderStructureSync(object):
    def __init__(self, src_root_full_path, destination_root_full_path):
        self.src_root_full_path = format_path(src_root_full_path)
        self.destination_root_full_path = format_path(destination_root_full_path)

    def get_target_folder(self, src_folder_full_path):
        relative_path = format_path(src_folder_full_path).replace(self.src_root_full_path, "")
        if relative_path[0] == "/":
            relative_path = relative_path[1:]
        target_full_path = format_path(os.path.join(self.destination_root_full_path, relative_path))
        ensure_dir(target_full_path)
        return target_full_path


if __name__ == "__main__":
    encrypted_folder_root = get_or_create_app_data_folder("tasty_pie_encrypted")
    file_path = os.path.join(encrypted_folder_root, "Richard-PC\\2013\\10\\09\\1381330659.94.7z")
    folder_path, encrypted_filename = os.path.split(file_path)
    d = DecZipFileOn7Zip(file_path, password=test_keys.password)
    file_list = d.list()
    decrypted_folder_root = get_or_create_app_data_folder("decrypted_data")
    sync = FolderStructureSync(encrypted_folder_root, decrypted_folder_root)
    for filename in file_list:
        output_folder = format_path(sync.get_target_folder(folder_path))
        d.extract_file(filename, output_folder)
