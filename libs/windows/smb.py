from ufsTreeItem import ufsTreeItemBase
import libSys
import libs.windows.netdisk.driver_mapping as driverMapping
import libs.ufsDb.dictShoveDb as dictShoveDb
import desktopApp.lib.localTreeItem as localTreeItem
import winUfs
import libs.utils.configurationTools as configurationTools


def removeHeadingSlash(s):
    while(s[0] == '\\'):
        s = s[1:]
    return s

class smbRootItem(ufsTreeItemBase):
    def isContainer(self, fullPath):
        '''
        return os.path.isdir(p)
        '''
        return True

    def child(self, fullPath):
        if fullPath == localDriverUuid:
            return localTreeItem.localWindowsRootItem()
        if fullPath == remoteDriverUuid:
            return []
            #return localTreeItem.localWindowsRootItem()
    def listNamedChildContainer(self):
        histDb = dictShoveDb.getDb("smbHistory")
        db = dictShoveDb.getDb("smbTmpInfo")
        s = driverMapping.sys_driver_mapping()
        m = s.get_mapping()
        res = {}
        mapping = {}
        hist = histDb["MappedResource"]
        
        #Add all existing mapped drivers in system
        for i in m:
            res[i+":/"] = m[i]
            mapping[m[i]] = i
            db[m[i]] = i
        #Add previous mapped drivers in database
        for i in hist:
            if not mapping.has_key(i):
                res["smb://"+i] = i
                mapping[i] = i
        hist = []
        #Add all history
        for i in mapping:
            hist.append(i)
        #Add history to storage
        histDb["MappedResource"] = hist
        return res


class smbTreeItem(localTreeItem.localTreeItem):
    def __init__(self, itemUrl):
        """
        ufsUrl = smb://mybook:pass@192.168.1.102/
        itemUrl = mybook:pass@192.168.1.102/
        """
        db = dictShoveDb.getDb("smbTmpInfo")
        try:
            userPass, server = itemUrl.split("@", 2)
            user, passwd = userPass.split(":",2)
        except ValueError:
            server = itemUrl
        server = server.replace("/",'\\')
        print server
        #Not mapped, map it
        #find an empty driver letter
        s = driverMapping.sys_driver_mapping()
        m = s.get_mapping()
        i = 'Z'
        while ord(i)>ord('A'):
            try:
                a = m[i]
            except KeyError:
                break
            i = chr(ord(i)-1)
        if ord(i) == ord('A'):
            raise "no driver letter available"
        print 'subst %s, %s'%(i, server)
        s.subst_driver(server, i)
        #Add ":/" to driver letter such as "C"+":/"
        self.fullPath = i+":/"
        self.parentDir = "winUfs"+configurationTools.getFsProtocolSeparator()+"%s"%winUfs.remoteDriverUuid



def getUfsTreeItem(itemUrl):
    return smbTreeItem(itemUrl)
    
    
def main():
    s = driverMapping.sys_driver_mapping()
    m = s.get_mapping()
    for i in m:
        print i+":"+s.mapping[i]
    #k = getUfsTreeItem("mybook:pass@192.168.1.102/public")
    getUfsTreeItem("\\\\q19420-03\\d$")
    m = s.get_mapping()
    for i in m:
        print i+":"+s.mapping[i]
     
if __name__ == '__main__':
    main()
