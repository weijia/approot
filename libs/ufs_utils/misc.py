import os


def ensure_dir(full_path):
    if not os.path.exists(full_path):
        os.makedirs(full_path)


gSupportedExt = ['jpg', 'avi']


def withExt(fullPath, extList=gSupportedExt):
    s = fullPath.split('.')
    if len(s) > 1:
        if s[-1].lower() in extList:
            #print fullPath, extList
            return True
    return False