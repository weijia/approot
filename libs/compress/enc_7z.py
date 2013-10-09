import os.path
import os

import subprocess
from libs.app_framework.folders import get_app_full_path_by_name

CREATE_NO_WINDOW = 0x8000000

gLocalEncode = 'gbk'


def encode2local(s):
    if type(s) == unicode:
        return s.encode(gLocalEncode)
    else:
        return s


def decode2local(s):
    return s.decode(gLocalEncode)


#Every app will be start in the root dir of the source code (prodRoot)
app = "..\\otherBin\\7za920\\7za.exe"


class EncZipFileOn7Zip(object):
    def __init__(self, file_path, mode="r", password='123'):
        self.file_path = file_path
        self.password = unicode(password)

    def addfile(self, adding_file, arcname=None):
        '''
        def ffmpegDumpVideo(inFile, outFile, frameTime = 10):
            cmd = (u'%s -y -i "%s" -f image2 -ss %d -vframes 1 -s 128x128 -an "%s"'%(app, inFile, frameTime, outFile)).encode('gbk')
            arg = (u' -y -i "%s" -f image2 -ss %d -vframes 1 -s 128x128 -an "%s"'%(inFile, frameTime, outFile)).encode('gbk')
            #os.system((u'%s -y -i "%s" -f image2 -ss %d -vframes 1 -s 128x128 -an "%s"'%(app, inFile, frameTime, outFile)).encode('gbk'))
            #return '%s -y -i "%s" -f image2 -ss 10 -vframes 1 -s 128x128 -an %s'%(app, inFile, outFile)
            #bufsize = 512
            #pipe = Popen(cmd, shell=True, bufsize=bufsize, stdout=PIPE).stdout
            #print pipe
            #process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            #    creationflags = subprocess.CREATE_NEW_CONSOLE|CREATE_NO_WINDOW)
            #retcode = subprocess.call([app, arg])
            #process = subprocess.Popen(cmd, shell=False)
            #CREATE_NO_WINDOW will hide the console window
            process = subprocess.Popen(cmd, shell=False, creationflags = CREATE_NO_WINDOW)
            #process = subprocess.Popen(cmd, shell=False)
            #wait is used to wait for the child process to complete
            process.wait()
            #sts = os.waitpid(process.pid, 0)[1]
            print (u'%s -y -i "%s" -f image2 -ss %d -vframes 1 -s 128x128 -an "%s"'%(app, inFile, frameTime, outFile)).encode('gbk')
        '''
        if os.path.exists(self.file_path):
            original_size = os.stat(self.file_path).st_size
        else:
            original_size = 0
        cmd = (u'%s -p%s -mhe a "%s" "%s"' % (get_app_full_path_by_name("7z"), self.password, self.file_path, adding_file)).encode(gLocalEncode)
        print "command:", cmd
        print "current dir:", os.getcwd()
        process = subprocess.Popen(cmd, shell=False, creationflags=CREATE_NO_WINDOW)
        #wait is used to wait for the child process to complete
        process.wait()
        increased_size = os.stat(self.file_path).st_size - original_size
        return increased_size

    def close(self):
        pass