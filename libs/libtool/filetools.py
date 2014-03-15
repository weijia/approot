import os
import time
import random
import re

#The following codes are copied from http://stackoverflow.com/questions/606561/how-to-get-filename-of-the-main-module-in-python
import imp
import sys


def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
            hasattr(sys, "importers") # old py2exe
            or imp.is_frozen("__main__")) # tools/freeze


def get_main_exec():
    if main_is_frozen():
        # print 'Running from path', os.path.dirname(sys.executable)
        return sys.executable
    return sys.argv[0]


def get_main_file():
    #print "----------------------", get_main_exec()
    # find path to where we are running
    return os.path.basename(get_main_exec()).split(".")[0]


def get_free_file_name(path, nameWithoutExt, ext):
    path_without_ext = os.path.join(path, nameWithoutExt)
    while os.path.exists(path_without_ext + ext):
        path_without_ext += '-' + str(random.randint(0, 10))
        #print thumb_path_without_ext
    return path_without_ext + ext


def get_free_name_from_full_path(full_path):
    """
    Just give a full path like: d:/good/bad.txt, generate a new path with a number in it and will not conflict with
    the files in that path. such as d:/good/bad-5.txt
    :param full_path:
    :return:
    """
    path = os.path.dirname(full_path)
    ext = os.path.splitext(full_path)[1]
    basename = os.path.basename(full_path)
    #print basename
    name_without_ext = basename[0:-(len(ext))]
    #print name_without_ext
    if name_without_ext == '':
        name_without_ext = basename
        ext = ''
    res = get_free_file_name(path, name_without_ext, ext)
    #print res
    return res


def get_free_timestamp_filename_in_path(path, ext, prefix=''):
    """
    Return a unused filename according to current time.
    :param path:
    :param ext: should start with "."
    :param prefix:
    :return:
    """
    #print path, ext, prefix
    filename = unicode(prefix + str(time.time()))
    return get_free_file_name(path, filename, ext)


def find_file_in_product(filename):
    p = os.getcwd()
    for dirpath, dirnames, filenames in os.walk(p):
        if filename in filenames:
            #print 'find file:', os.path.join(dirpath, filename)
            return os.path.join(dirpath, filename)
    return None


def find_filename_in_app_framework_with_pattern(pattern):
    p = os.getcwd()
    #print 'current path:', p
    for dirpath, dirnames, filenames in os.walk(p):
        for i in filenames:
            res = re.search(pattern, i)
            #print pattern, i
            if res is None:
                continue
                #print 'found item:', pattern, i
            return os.path.join(dirpath, i)
    print "path not found", pattern
    return None


def find_callable_in_app_framework(filename):
    #filename = filename.replace('-', '\-')
    return find_filename_in_app_framework_with_pattern('^' + filename + "((\.bat$)|(\.py$)|(\.exe$)|(\.com$))")


def collect_files_in_dir(file_root_full_path, ext=None, ignore_file_list=[]):
    res = []
    if os.path.exists(file_root_full_path) and os.path.isdir(file_root_full_path):
        for filename in os.listdir(file_root_full_path):
            if filename in ignore_file_list:
                print "ignoring: ", filename
                continue
            if (ext is None) or (ext in filename):
                #To ensure .pyc is not included
                if len(filename.split(ext)[1]) != 0:
                    continue
                full_path = os.path.join(file_root_full_path, filename)
                print full_path
                res.append(full_path)
    return res


def get_app_name_from_full_path(app_path):
    app_filename = os.path.basename(app_path)
    app_name = app_filename.split(".")[0]
    return app_name