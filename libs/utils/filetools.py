import os
import time
import random
import re

def getFreeName(path, nameWithoutExt, ext):
    path_without_ext = os.path.join(path, nameWithoutExt)
    while os.path.exists(path_without_ext+ext):
        path_without_ext += '-' + str(random.randint(0,10))
        #print thumb_path_without_ext
    return path_without_ext+ext

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
  
def getTimestampWithFreeName(path, ext, prefix = ''):
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
    return findNamePatternInProduct('^'+filename+"((\.bat$)|(\.py$)|(\.exe$)|(\.com$))")