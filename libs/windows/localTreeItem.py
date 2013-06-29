import os
import windowsDriver
from localTreeItemBase import localTreeItemBase as localTreeItemBase
from localTreeItemBase import localFilesystemDecode as localFilesystemDecode

gWinRootUuid = '8df322ad-2cab-4393-a66c-e5b9b24e4324'


class localWindowsRootItem(localTreeItemBase):
    def getContainerItem(self):
        return None
    def isChildContainer(self, p):
        return self.isContainer(p)
    def isContainer(self, p):
        try:
            os.listdir(p)
            return True
        except WindowsError:
            return False
        
    def listSortedChildren(self):
        res = windowsDriver.getDriverList()
        drivers = {}
        for i in res:
            drivers[i+'/'] = i+'/'
        return drivers
    def getName(self, p):
        return p
    def listNamedChildren(self, start = 0, cnt = None, getParent = True):
        return self.listSortedChildren()


class localTreeItem(localTreeItemBase):
    def __init__(self, fullPath):
        self.fullPath = fullPath
        #print 'creating dir elem:%s'%fullPath.encode('utf8')
        if gWinRootUuid == fullPath:
            self.parentDir = None
        else:
            self.parentDir = os.path.dirname(self.fullPath)
        
    def getContainerItem(self):
        return self.parentDir

        
    def listNamedChildren(self):
        if not os.path.isdir(self.fullPath):
            #print 'not n dir'
            return None
        res = {}
        d = os.listdir(self.fullPath)
        #print d
        for i in d:
            res[os.path.join(self.fullPath, i)] = localFilesystemDecode(i)
        return res
    def listSortedChildren(self):
        if not os.path.isdir(self.fullPath):
            #print 'not a dir'
            return []
            #return ['..']
        res = []
        d = os.listdir(self.fullPath)
        #print d
        for i in d:
            res.append(os.path.join(self.fullPath, i))
        return res
        
    def listNamedChildContainer(self):
        if not os.path.isdir(self.fullPath):
            #print 'not n dir'
            return None
        res = {}
        d = os.listdir(self.fullPath)
        #print d
        for i in d:
            if os.path.isdir(os.path.join(self.fullPath, i)):
                res[localFilesystemDecode(os.path.join(self.fullPath, i))] = localFilesystemDecode(i)
        return res
    def isContainer(self, p):
        try:
            for i in os.listdir(p):
                if os.path.isdir(os.path.join(p, i)):
                    return True
        except:
            pass
        return False