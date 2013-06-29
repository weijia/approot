from PyQt4.QtGui import QStandardItemModel
from PyQtConsoleOutputWnd import MinimizeOnClose, ToggleMaxMin
from PyQt4 import QtCore, QtGui, uic
import libsys
import libs.utils.filetools as filetools
    
class ApplicationList(QtGui.QWidget, MinimizeOnClose, ToggleMaxMin):
    msg_signal = QtCore.pyqtSignal(object)
    ################################################
    #Msg related functions
    '''
    def trigger(self, msg):
        self.msg_signal.emit(msg)
    '''

    def set_msg_callback(self, callback):
        self.customer_msg_callback = callback
        
    def msg_callback(self, msg):
        #print "msg_callback in main thread called:", msg
        self.customer_msg_callback(msg)

    def __init__(self):
        super(ApplicationList, self).__init__()
        ui_full_path = filetools.findFileInProduct('app_list.ui')
        self.ui = uic.loadUi(ui_full_path, self)
        self.model = QStandardItemModel()
        '''
        item = QStandardItem('Hello world')
        item1 = QStandardItem('Hello world1')
        item.setCheckState(Qt.Checked)
        item.setCheckable(True)
        item1.setCheckState(Qt.Checked)
        item1.setCheckable(True)
        self.model.appendRow(item)
        self.model.appendRow(item1)
        '''
        self.listView.setModel(self.model)
        '''
        self.connect(self.listView.selectionModel(),  
                     QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),  
                     self.store_current_selection) 
        '''
        #self.show()
        self.listView.clicked.connect(self.item_clicked)
        self.minimized = True
        self.msg_signal.connect(self.msg_callback)


    def item_clicked(self, index):
        self.callback_func(str(self.model.item(index.row()).text()))

    def set_callback(self, callback_func):
        self.callback_func = callback_func
