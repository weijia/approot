import os

def findFileInProduct(filename):
    p = os.getcwd()
    for dirpath, dirnames, filenames in os.walk(p):
        if filename in filenames:
            #print 'find file:', os.path.join(dirpath, filename)
            return os.path.join(dirpath, filename)
    return None
