import os
import re
import libsys
import libs.utils.transform as transform

from libs.services.apps.tube_folder_tagging import add_tag_for_full_path
from libs.obj_related.local_obj import LocalObj

g_default_thumb_size = 256

class pictureFormatNotSupported:
    pass

        
def picFormatSupportedV2(full_path, mime_type = None):
    if mime_type is None:
        res = LocalObj(full_path).get_type()
    else:
        res = mime_type
    #print res
    if res.find('image') != -1:
        #print 'image', full_path
        return True
    else:
        print "mime type have no thumb:", res
        return False
        
def genPicThumb(local_path, dest_dir, mime_type = None):
    #If no thumbnail exist, create one
    #print '-----------------------localpath:',local_path
    basename = os.path.basename(local_path)
    #print "basename:" + basename
    
    ext = basename.split(".")[-1]
    #print ext
    if picFormatSupportedV2(local_path, mime_type = None):
        add_tag_for_full_path(local_path, "system:pic", "app:thumb_generator")
        #It is a jpeg file, currently no other type supported
        if os.path.getsize(local_path) < 10*1024:
            #Use the original file if its siez is small
            return transform.transformDirToInternal(local_path)
        from PIL import Image #Using PIL lib
        im = Image.open(local_path)
        # convert to thumbnail image
        im.thumbnail((g_default_thumb_size, g_default_thumb_size), Image.ANTIALIAS)
        # don't save if thumbnail already exists
        #Use _T as the thumb file end to indicate the end of the original firl
        thumb_path_without_ext = os.path.join(dest_dir, basename.split(".")[0]+"_T")
        import random
        while os.path.exists(thumb_path_without_ext+".jpg"):
            thumb_path_without_ext += str(random.randint(0,10))
        thumb_path = thumb_path_without_ext+'.jpg'
        #print thumb_path.encode("utf8","replace")
        if im.mode != "RGB":
            im = im.convert("RGB")
        im.save(thumb_path,  "JPEG")
        return transform.transformDirToInternal(thumb_path)
    else:
        print 'non jpeg file not supported'
        raise pictureFormatNotSupported
    

def returnThumbString(local_path):
    import Image #Using PIL lib 
    import cStringIO
    import StringIO
    im = Image.open(local_path)
    # convert to thumbnail image
    im.thumbnail((128, 128), Image.ANTIALIAS)
    f = cStringIO.StringIO()
    im.save(f,  "JPEG")
    return f