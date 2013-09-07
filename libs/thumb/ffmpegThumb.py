import subprocess
#from subprocess import *
import os
from libs.tags.views import add_tag_for_full_path


app = "..\\others\\ffmpeg\\bin\\ffmpeg.exe"
CREATE_NO_WINDOW = 0x8000000


def ffmpegDumpVideo(inFile, outFile, frameTime=10):
    cmd = (u'%s -y -i "%s" -f image2 -ss %d -vframes 1 -s 256x256 -an "%s"' % (app, inFile, frameTime, outFile)).encode(
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
    process = subprocess.Popen(cmd, shell=False, creationflags=CREATE_NO_WINDOW)
    #process = subprocess.Popen(cmd, shell=False)
    #wait is used to wait for the child process to complete
    process.wait()
    #sts = os.waitpid(process.pid, 0)[1]
    print (u'%s -y -i "%s" -f image2 -ss %d -vframes 1 -s 128x128 -an "%s"' % (app, inFile, frameTime, outFile)).encode(
        'gbk')


def genVideoThumb(local_path, dest_dir):
    #The ffmpeg application seems do not support output filename including %
    basename = os.path.basename(local_path).replace('%', '_')
    thumb_path_without_ext = os.path.join(dest_dir, basename.split(".")[0] + "_T")
    import random

    while os.path.exists(thumb_path_without_ext + u".jpg"):
        thumb_path_without_ext += unicode(random.randint(0, 10))
    thumb_path = thumb_path_without_ext + u'.jpg'
    ffmpegDumpVideo(local_path, thumb_path)
    #print thumb_path.encode('gbk', 'replace')
    if not os.path.exists(thumb_path):
        ffmpegDumpVideo(local_path, thumb_path, 1)
    if os.path.exists(thumb_path):
        add_tag_for_full_path(local_path, "system:video", "app:thumb_generator")
        return thumb_path
    return None


if __name__ == '__main__':
    genVideoThumb('G:/app/wwj.wmv', "d:/tmp")