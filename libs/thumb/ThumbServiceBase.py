import picThumbGenerator
#import movieThumb
import ffmpegThumb
import appThumb
import os
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
                    pass
            else:
                pass
    if newPath is None:
        return None
    return transformDirToInternal(newPath)

class ThumbServiceBase(object):
    def __init__(self, db_sys):
        self.db_sys = db_sys
        self.src_to_thumb_db = self.db_sys.getDb("src_to_thumb_db")
        self.thumb_to_src_db = self.db_sys.getDb("thumb_to_src_db")
    def set_thumb_cache(self, src_full_path, thumb_url):
        self.src_to_thumb_db.append(src_full_path, thumb_url)
        self.thumb_to_src_db[thumb_url] = src_full_path
    
    def get_thumb(self, src_full_path, target_dir, mime_type = None):
        thumb_path = self.get_cached_thumb(src_full_path)
        if thumb_path is None:
            try:
                thumb_path = internal_get_thumb(src_full_path, target_dir, mime_type)
            except:
                traceback.print_exc()
            if thumb_path is None:
                return None
            self.set_thumb_cache(src_full_path, thumb_path)
            return thumb_path
        else:
            return thumb_path

    def get_cached_thumb(self, src_full_path):
        try:
            for thumb_full_path in self.src_to_thumb_db[src_full_path]:
                if os.path.exists(thumb_full_path):
                    return thumb_full_path
        except KeyError:
            ncl(src_full_path, "not in cache")
            pass
        return None


def getThumb(path, targetDir = gWorkingDir, mime_type = None, req = None):
    if req is None:
        import wwjufsdatabase.libs.services.servicesV2 as service
        req = service.req()
    #We can have a database from the req. So save the thumb info.
    t = ThumbServiceBase(req.getDbSys())
    if isUfsFs(path):
        full_path = getPathForUfsUrl(path)
    else:
        full_path = path
    #cl(path)
    full_path = transformDirToInternal(full_path)
    return t.get_thumb(full_path, targetDir, mime_type)
        