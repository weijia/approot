import win32ui
import win32gui
import win32con
import win32api
import cStringIO
from PIL import Image
import os
import libs.utils.filetools as fileTools



def genAppThumb(local_path, dest_dir):
  basename = os.path.basename(local_path)
  nameWithoutExt = basename.rsplit(".", 2)[0]
  thumb_path = fileTools.getFreeName(dest_dir, nameWithoutExt, ".bmp")
  getIcon(local_path, thumb_path)
  if os.path.exists(thumb_path):
    return thumb_path
  return None


def getIcon(path, targetFullPath):
    #tempDirectory = os.getenv("temp")
    ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
    #print targetFullPath
    large, small = win32gui.ExtractIconEx(path,0)
    try:
        win32gui.DestroyIcon(small[0])
    except:
        pass
    #creating a destination memory DC
    hdc = win32ui.CreateDCFromHandle( win32gui.GetDC(0) )
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_x)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject( hbmp ) #draw a icon in it
    hdc.DrawIcon( (0,0), large[0] )
    win32gui.DestroyIcon(large[0])
    #convert picture
    hbmp.SaveBitmapFile( hdc, targetFullPath)
    '''
    im = Image.open(tempDirectory + "\Icontemp.bmp")
    im.save(targetFullPath, "PNG")
    os.remove(tempDirectory + "\Icontemp.bmp")
    '''
    
if __name__ == '__main__':
    genAppThumb("D:\\TDDOWNLOAD\\Software\\Q-Dir_4.4.2.exe", "d:/tmp")