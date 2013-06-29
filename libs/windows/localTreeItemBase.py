import os

def localFilesystemDecode(i):
    if type(i) == unicode:
        return i
    return i.decode('gbk','replace')

gFileSystemRootUuid = 'ff76d539-72bf-4d51-a543-ea4f1effd5ad'

class localTreeItemBase:
    def getContainerItem(self):
        return self.parentDir
        
    def getChildAbsPath(self, p):
        return p
        
    def getName(self, p):
        return os.path.basename(p)
        
    def isContainer(self, p):
        '''
        return os.path.isdir(p)
        '''
        try:
            l = os.listdir(p)
            if len(l) > 0:
                return True
            return False
        except WindowsError:
            return False

    def child(self, fullPath):
        return localTreeItem(fullPath)