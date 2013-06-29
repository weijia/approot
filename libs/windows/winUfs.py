import libSys
import wwjufsdatabase.libs.ufs.ufsTreeItem as ufsTreeItem
try:
    from google.appengine.ext import webapp
except ImportError:
    import sys
    import os
    c = os.getcwd()
    while c.find('prodRoot') != -1:
      c = os.path.dirname(c)
    #print c
    sys.path.insert(0, os.path.join(c,'prodRoot'))
    import localLibs.windows.localTreeItem as localTreeItem

import libs.utils.configurationTools as configurationTools

localDriverUuid = u'290b5fcc-be54-4ae4-9613-20a24de723cf'
remoteDriverUuid = u'9ee70015-bfef-44ee-8d1c-48a4e6399954'
winUfsRootItemUuid = u'7c030fb5-8094-48fa-b9db-827ba90668ef'

localDriverName = u"Local Driver"
remoteDriverName = u"Remote Driver"
#import smb

class winUfsTreeItem(ufsTreeItem.ufsTreeItemBase):
    def isContainer(self, fullPath):
        '''
        return os.path.isdir(p)
        '''
        return True
    def isChildContainer(self, childPath):
        '''
        return os.path.isdir(p)
        '''
        return True
    def child(self, fullPath):
        if fullPath == winUfsRootItemUuid:
            return winUfsTreeItem()
        if fullPath == localDriverUuid:
            return localTreeItem.localWindowsRootItem()
        if fullPath == remoteDriverUuid:
            return smb.smbRootItem()
            #return localTreeItem.localWindowsRootItem()
    def listNamedChildren(self, start = 0, cnt = None, getParent = True):
        #Return {fullPath:name}
        res = {u"winUfs"+configurationTools.getFsProtocolSeparator()+"%s"%localDriverUuid:localDriverName,
            u"winUfs"+configurationTools.getFsProtocolSeparator()+"%s"%remoteDriverUuid:remoteDriverName
        }
        return res

def getUfsTreeItem(itemUrl, req):
    return winUfsTreeItem().child(itemUrl)


def getUfsCollection(itemUrl, req):
    return winUfsTreeItem().child(itemUrl)