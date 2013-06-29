from PyQt4.QtGui import QStandardItemModel, QStandardItem
from PyQt4.QtCore import  Qt
from PyQtConsoleOutputWnd import MinimizeOnClose, ToggleMaxMin
from PyQt4 import QtCore, QtGui, uic
import sys
import libsys
import libs.utils.filetools as filetools
from configuration import g_config_dict

class DroppableMain(QtGui.QMainWindow):
    def __init__(self):
        super(DroppableMain, self).__init__()
        self.show() 

def main():
    app = QtGui.QApplication(sys.argv)
    dropable = Droppable()
    main = DroppableMain()
    sys.exit(app.exec_())
    
#Codes got from http://stackoverflow.com/questions/7138773/draggable-window-with-pyqt4
class Draggable:
    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x-x_w, y-y_w)

class Droppable(QtGui.QWidget, Draggable):

    def __init__(self):
        super(Droppable, self).__init__()
        ui_full_path = filetools.findFileInProduct('droppable.ui')
        self.ui = uic.loadUi(ui_full_path, self)
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint|QtCore.Qt.Tool|QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.X11BypassWindowManagerHint)
        self.setAcceptDrops(True)
        #print '-------------------------------------', g_config_dict["drop_wnd_color"]
        if not (g_config_dict["drop_wnd_color"] is None):
            #QtGui.QWidget.setBackground(self, QtGui.QColor(g_config_dict["drop_wnd_color"]))
            #self.setBackgroundRole(QtGui.QPalette.Dark);
            p = self.palette()
            p.setColor(self.backgroundRole(), Qt.red)
            self.setPalette(p)
            self.setAutoFillBackground(True);
        self.setGeometry(300,300,30,30)
        self.show()
        self.drop_callback = None

    def dragEnterEvent(self, e):
        '''
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore() 
        '''
        e.accept()
    def set_drop_callback(self, drop_callback):
        self.drop_callback = drop_callback
        
    def dropEvent(self, e):
        print e.mimeData().urls()
        if self.drop_callback is None:
            return
        res = []
        for i in e.mimeData().urls():
            res.append(unicode(i.toString()))
        self.drop_callback(self, res)
        
if __name__ == '__main__':
    main()

