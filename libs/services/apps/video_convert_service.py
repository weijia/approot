'''
@author: Richard
'''
from os.path import basename
import subprocess
import os
from libs.utils.objTools import get_ufs_obj_from_full_path
import libsys
from libs.logsys.logSys import cl
from libs.services.svc_base.msg_service import MsgQ
from libs.services.svc_base.simple_service_v2 import SimpleService, SimpleServiceWorker

CREATE_NO_WINDOW = 0x8000000
app = "..\\others\\ffmpeg\\bin\\ffmpeg.exe"


def ffmpegDumpVideo(inFile, outFile):
    cmd = (u'%s -y -i "%s" -s 320x240 "%s"' % (app, inFile, outFile)).encode(
        'gbk')
    #arg = (u' -y -i "%s" -f image2 -ss %d -vframes 1 -s 256x256 -an "%s"'%(inFile, frameTime, outFile)).encode('gbk')
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
    #process = subprocess.Popen(cmd, shell=False, creationflags=CREATE_NO_WINDOW)
    process = subprocess.Popen(cmd, shell=False)
    #wait is used to wait for the child process to complete
    process.wait()
    #sts = os.waitpid(process.pid, 0)[1]


class VideoConvertThread(SimpleServiceWorker):
    def on_register_ok(self):
        super(VideoConvertThread, self).on_register_ok()
        import libs.utils.misc as misc
        target_data_folder_name = "converted"
        self.target_dir = os.path.join(libsys.get_root_dir(), "../"+target_data_folder_name)
        misc.ensureDir(self.target_dir)

    def process(self, msg):
        obj = get_ufs_obj_from_full_path(msg.get_path())
        import libs.utils.filetools as file_tools
        expecting_path = os.path.join(self.target_dir, basename(obj.full_path))
        expecting_path = file_tools.getFreeNameFromFullPath(expecting_path)
        cl("Start to convert file:", obj.full_path)
        ffmpegDumpVideo(obj.full_path, expecting_path)
        cl("Convert ended for:", expecting_path)
        return True


if __name__ == "__main__":
    s = SimpleService({
                          "input": "input tube name",
                          "output": "output tube name, optional",
                          #"blacklist": "blacklist for scanning, example: *.exe",
                      },
                      worker_thread_class=VideoConvertThread)
    s.run()