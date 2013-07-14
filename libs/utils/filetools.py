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


def getFreeName(path, nameWithoutExt, ext):
    path_without_ext = os.path.join(path, nameWithoutExt)
    while os.path.exists(path_without_ext + ext):
        path_without_ext += '-' + str(random.randint(0, 10))
        #print thumb_path_without_ext
    return path_without_ext + ext


def getFreeNameFromFullPath(fullPath):
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


def getTimestampWithFreeName(path, ext, prefix=''):
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
    return None


def findAppInProduct(filename):
    #filename = filename.replace('-', '\-')
    return findNamePatternInProduct('^' + filename + "((\.bat$)|(\.py$)|(\.exe$)|(\.com$))")