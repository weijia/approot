import libsys
import libs.utils.filetools as fileTools
import libs.utils.misc as misc
import os
import configuration


class logDir:
    def __init__(self, logName, logRootPath = configuration.log_root, maxLogFile = 10):
        self.logName = logName.replace("\\","_").replace("/","_").replace(":","_").replace("'","").replace('"',"").replace("?","").replace("*","").replace(" ","")
        self.logFullPath = os.path.join(logRootPath, self.logName)
        self.maxLogFile = maxLogFile
        misc.ensure_dir(self.logFullPath)
    def getLogFilePath(self):
        fileList = {}
        numberList = []
        for i in os.listdir(self.logFullPath):
            try:
                number = float(i.replace(".log",""))
            except:
                continue
            fileList[number] = i
            numberList.append(number)
        numberList.sort()
        #print numberList
        deleteLen = len(numberList) - self.maxLogFile
        #print deleteLen
        if deleteLen >= 0:
            #Delete old ones
            for i in numberList[0:deleteLen+1]:
                #print 'deleting:', i
                try:
                    os.remove(os.path.join(self.logFullPath, fileList[i]))
                except WindowsError:
                    pass
        return fileTools.get_free_timestamp_filename_in_path(self.logFullPath, '.log')
        
        
if __name__ == '__main__':
    l = logDir("testLogDir")
    f = open(l.getLogFilePath(),'w')
    f.close()
            
            