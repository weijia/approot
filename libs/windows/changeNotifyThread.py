import threading
import os
import sys
import datetime
import time

import win32file
import win32con
import cPickle
from stat import ST_SIZE
#from dbus.mainloop.glib import threads_init
import libsys
from libs.logsys.logSys import *

ACTIONS = {
  1 : "Created",
  2 : "Deleted",
  3 : "Updated",
  4 : "Renamed from something",
  5 : "Renamed to something"
}


#Reference: http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html
class changeNotifyThread(threading.Thread):
    def __init__ ( self, fullPath):
        self.path_to_watch = fullPath
        super(changeNotifyThread, self).__init__ ()

    def run ( self ):
        #threads_init()
        self.need_to_quit = False
        self.path_to_watch = os.path.abspath (self.path_to_watch)
        info("Watching %s at %s" % (self.path_to_watch, time.asctime ()))
        hDir = win32file.CreateFile(
            self.path_to_watch,
            win32con.GENERIC_READ,
            win32con.FILE_SHARE_READ|win32con.FILE_SHARE_WRITE,
            None,
            win32con.OPEN_EXISTING,
            win32con.FILE_FLAG_BACKUP_SEMANTICS,
            None
        )
        cnt = 0
        while not self.need_to_quit:
#            print "new watch\n"
            results = win32file.ReadDirectoryChangesW(
                hDir,
                1024,
                True,
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME
                | win32con.FILE_NOTIFY_CHANGE_DIR_NAME
                | win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES
                | win32con.FILE_NOTIFY_CHANGE_SIZE
                | win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
                | win32con.FILE_NOTIFY_CHANGE_SECURITY,
                None,
                None
            )
            if not self.need_to_quit:
                for action, file in results:
                    #full_filename = os.path.join (self.path_to_watch, file)
                    #print full_filename, ACTIONS.get (action, "Unknown")
                    self.callback(self.path_to_watch, file, ACTIONS.get (action, "Unknown"))
                    
    def callback(self, pathToWatch, relativePath, action):
        pass
        
    def exit(self):
        self.need_to_quit = True
