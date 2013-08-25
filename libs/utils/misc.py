import os
import time
import libs.utils.transform as transform
import libs.utils.filetools as fileTools

def ensure_dir(fullPath):
    if not os.path.exists(fullPath):
        os.makedirs(fullPath)

        
        
gSupportedExt = ['jpg','avi']

def withExt(fullPath, extList = gSupportedExt):
    s = fullPath.split('.')
    if len(s) > 1:
        if  s[-1].lower() in extList:
            #print fullPath, extList
            return True
    return False

def get_prot_root():
    c = os.getcwd()
    while c.find('prodRoot') != -1:
        c = os.path.dirname(c)
    return os.path.join(c,'prodRoot')


def get_date_based_path(root_folder, ext = ".7z"):
    gTimeV = time.gmtime()
    yearStr = time.strftime("%Y", gTimeV)
    monthStr = time.strftime("%m", gTimeV)
    dayStr = time.strftime("%d", gTimeV)
    dateTimeDir = yearStr+"/"+monthStr+"/"+dayStr
    newEncDir = unicode(os.path.join(root_folder, dateTimeDir))
    ensure_dir(newEncDir)
    file_full_path = transform.transformDirToInternal(
        fileTools.getTimestampWithFreeName(newEncDir, ext))
    return file_full_path
