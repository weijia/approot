# -*- coding: utf-8 -*-  
from PyQtConsoleOutputWnd import PyQtConsoleOutputWnd
import PyQt4.QtGui as QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from TaskbarIcon import List2SystemTray, ConsoleManager
from PyQt4 import QtCore
import fileTools
from droppable import Droppable
from browser import Browser
class GuiFactoryBase(object):
    def __init__(self):
        pass
        
    def create_taskbar_icon_app(self):
        pass
        
    def create_console_output_wnd(self, parent, logFilePath = None):
        pass
    def start_msg_loop(self):
        pass
    def get_app_list(self):
        pass

class PyQtGuiFactory(GuiFactoryBase):
    def __init__(self):
        super(PyQtGuiFactory, self).__init__()
        self.app = QtGui.QApplication(sys.argv)
        self.droppable_list = []
        self.browser_list = {}
        
    ################################################
    #Msg related functions
    def trigger(self, msg):
        #print "trigger called:", msg
        self.console_man.app_list.msg_signal.emit(msg)
        
        
    def set_msg_callback(self, callback):
        self.console_man.app_list.set_msg_callback(callback)
        
    ################################################
    #GUI related
    def create_taskbar_icon_app(self):
        self.w = QtGui.QWidget()
        icon_full_path = fileTools.findFileInProduct("gf-16x16.png")
        self.trayIcon = List2SystemTray(QtGui.QIcon(icon_full_path), self.w)
        #self.trayIcon["Example"] = exampleAction
        return self.trayIcon
        
    def create_console_output_wnd(self, parent, logFilePath = None):
        return PyQtConsoleOutputWnd(parent, logFilePath)
        
    def start_msg_loop(self):
        sys.exit(self.app.exec_())
        print "existing msg loop"
    def timeout(self, milliseconds, callback):
        self.ctimer = QtCore.QTimer()
        # constant timer
        QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), callback)
        self.ctimer.start(milliseconds)
    def exit(self):
        QtGui.QApplication.quit()
    def get_app_list(self):
        self.console_man = ConsoleManager()
        return self.console_man
    def create_drop_target(self, callback):
        droppable_wnd = Droppable()
        self.droppable_list.append(droppable_wnd)
        droppable_wnd.set_drop_callback(callback)
        return droppable_wnd
    def show_browser(self, handle, url):
        #when calling load, url will be quoted? Seems yes.
        if self.browser_list.has_key(handle):
            self.browser_list[handle].load(QUrl(url))
            self.browser_list[handle].show()
            self.browser_list[handle].raise_()
            self.browser_list[handle].activateWindow()
        else:
            web = Browser()
            web.load(QUrl(url))
            #print "pyqt opening: ", url
            #web.load(QUrl("http://baidu.com"))
            self.browser_list[handle] = web
            web.show()
            web.raise_()
            web.activateWindow()
        #objWebSettings = self.browser_list[handle].settings();
        #print objWebSettings.defaultTextEncoding();
        #print objWebSettings.fontFamily(0)
        #objWebSettings.setFontFamily(0, 'ËÎÌו')
        #objWebSettings.setDefaultTextEncoding("gbk");
    def msg(self, msg):
        self.trayIcon.msg(msg)
        