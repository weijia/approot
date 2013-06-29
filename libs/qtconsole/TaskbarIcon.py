import sys
from PyQt4 import QtGui
from PyQt4.QtGui import QApplication
from PyQt4 import QtCore
from PyQt4.QtGui import QStandardItem
from PyQt4.QtCore import  Qt
from notification import Notification

class SystemTrayIcon(QtGui.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = QtGui.QMenu(parent)
        #exitAction = self.menu.addAction("Exit")
        #exitAction.triggered.connect(self.exitHandler)
        self.setContextMenu(self.menu)
    #def exitHandler(self):
    #    QApplication.quit()
        
        
import UserDict
from applist import ApplicationList
        
class List2SystemTray(UserDict.DictMixin):
    def __init__(self, icon, parent=None):
        self.systemTrayIcon = SystemTrayIcon(icon, parent)
        self.systemTrayIcon.show()
        self.actionDict = {}
        #self.msg("App started")
        
    def __setitem__(self, key, value):
        action = self.systemTrayIcon.menu.addAction(key)
        action.triggered.connect(value)
        self.actionDict[key] = value
    def __delitem__(self, key):
        action = self.systemTrayIcon.menu.removeAction(key)
        action.triggered.connect(value)
        del self.actionDict[key]
    
    def msg(self, msg):
        #self.systemTrayIcon.showMessage("Ufs system", msg, 20000)
        try:
            self.mynotif = Notification()
        except:
            import traceback
            traceback.print_exc()
        self.mynotif.noti(msg)
    

class ConsoleManager(UserDict.DictMixin):
    def __init__(self):
        self.app_list = ApplicationList()
        self.app_list.set_callback(self.app_list_callback)
        self.actionDict = {}
        self.item_dict = {}
        self.key2item = {}
        
        #self.app_list.show()
    def show_app_list(self):
        self.app_list.show()
        
    def __setitem__(self, key, value):
        if self.item_dict.has_key(key):
            item = self.key2item[key]
            #item.setCheckable(value["checked"])
        else:
            item = QStandardItem(key)
            item.setCheckable(True)
            #item.setCheckable(value["checked"])
            self.app_list.model.appendRow(item)
        if value["checked"]:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)
        self.actionDict[key] = value["action"]
        self.item_dict[key] = value
        self.key2item[key] = item
        
    def __getitem__(self, key):
        if not isinstance(key, basestring):
            raise "not string"
        return self.key2item[key]
        
    def app_list_callback(self, str):
        #print 'callback called:', str
        self.actionDict[str](str)

def main():
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QWidget()
    trayIcon = List2SystemTray(QtGui.QIcon("gf-16x16.png"), w)
    console_man =  ConsoleManager()
    trayIcon["Applications"] = console_man.show_app_list
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()