import os
import time
import random
import re

#The following codes are copied from http://stackoverflow.com/questions/606561/how-to-get-filename-of-the-main-module-in-python
import imp
import sys
import libsys


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


def getFreeName(path, nameWithoutExt, ext):
    path_without_ext = os.path.join(path, nameWithoutExt)
    while os.path.exists(path_without_ext + ext):
        path_without_ext += '-' + str(random.randint(0, 10))
        #print thumb_path_without_ext
    return path_without_ext + ext


def getFreeNameFromFullPath(fullPath):
    """
    Just give a full path like: d:/good/bad.txt, generate a new path with a number in it and will not conflict with
    the files in that path. such as d:/good/bad-5.txt
    :param fullPath:
    :return:
    """
    path = os.path.dirname(fullPath)
    ext = os.path.splitext(fullPath)[1]
    basename = os.path.basename(fullPath)
    #print basename
    nameWithoutExt = basename[0:-(len(ext))]
    #print nameWithoutExt
    if nameWithoutExt == '':
        nameWithoutExt = basename
        ext = ''
    res = getFreeName(path, nameWithoutExt, ext)
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
    return getFreeName(path, filename, ext)


def findFileInProduct(filename):
    p = os.getcwd()
    for dirpath, dirnames, filenames in os.walk(p):
        if filename in filenames:
            #print 'find file:', os.path.join(dirpath, filename)
            return os.path.join(dirpath, filename)
    return None


def findNamePatternInProduct(pattern):
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


def findAppInProduct(filename):
    #filename = filename.replace('-', '\-')
    return findNamePatternInProduct('^' + filename + "((\.bat$)|(\.py$)|(\.exe$)|(\.com$))")


def collect_files_in_dir(file_root_path, ext=None, ignoreFileList=[]):
    res = []
    if file_root_path[0] == "/":
        file_root_path = file_root_path[1:]
    file_root_path = os.path.join(libsys.get_root_dir(), file_root_path)
    print file_root_path
    if os.path.exists(file_root_path) and os.path.isdir(file_root_path):
        for filename in os.listdir(file_root_path):
            if filename in ignoreFileList:
                print "ignoring: ", filename
                continue
            if (ext is None) or (ext in filename):
                #To ensure .pyc is not included
                if len(filename.split(ext)[1]) != 0:
                    continue
                full_path = os.path.join(file_root_path, filename)
                print full_path
                res.append(full_path)
    return res
