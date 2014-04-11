import picThumbGenerator
#import movieThumb
import ffmpegThumb
try:
    import appThumb
except ImportError:
    appThumb = None
from ufs_utils.transform import format_path
from ufs_utils.obj_tools import isUfsFs, getPathForUfsUrl
import traceback


g_non_video_file_ext_list = ["7z", "apk","asp", "aspx", "cab", "chm", "c", "class", "cpp", "crx", 
                             "doc", "docx", "dll", 
                             "h", "hpp", "egg", "iso", "java", "html", "gz", "img", 
                             "log","php", 
                             "sis", "sisx", "py", "pyc", "htm",
                             "tar","txt", "rar", "pdf", 
                             "msi", "jar", "xpi", "mp3", "wav",
                             "ogg", "ini", "sys", "db", "m", "rtf", "xls", "xlsx",  "zip"]

g_video_file_ext_list = ["mov", "avi", "mkv", "mp4", "flv", "rm", "rmvb"]

gWorkingDir = "d:/tmp/working/thumbs"

def internal_get_thumb(path, targetDir, mime_type = None):
    '''
    path: Full Path. The path of the file whose thumbnail will be generated
    targetDir: Directory Path. The target directory where the generated thumbnail will be put in.
    Return: the thumbnail fullPath
    '''
    newPath = None
    ext = path.split('.')[-1].lower()
    if ext in ['exe']:
        try:
            newPath = appThumb.genAppThumb(path, targetDir)
        except:
            return None
    else:
        try:
            newPath = picThumbGenerator.genPicThumb(path, targetDir, mime_type)
        except picThumbGenerator.pictureFormatNotSupported:
            if ext in g_video_file_ext_list:
                try:#if True:
                        newPath = ffmpegThumb.genVideoThumb(path, targetDir)
                        #return "complete transform"
                        #return newPath
                except:
                    import traceback
                    traceback.print_exc()
            else:
                pass
    if newPath is None:
        return None
    return format_path(newPath)


def get_thumb(path, targetDir = gWorkingDir, mime_type = None, req = None):
    if isUfsFs(path):
        full_path = getPathForUfsUrl(path)
    else:
        full_path = path
    #cl(path)
    full_path = format_path(full_path)
    return internal_get_thumb(full_path, targetDir, mime_type)