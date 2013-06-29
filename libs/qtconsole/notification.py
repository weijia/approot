from PyQt4.QtGui import QStandardItemModel
from PyQtConsoleOutputWnd import MinimizeOnClose, ToggleMaxMin
from PyQt4 import QtCore, QtGui, uic
import libsys
import libs.utils.filetools as filetools
    
class Notification(QtGui.QWidget, MinimizeOnClose, ToggleMaxMin):
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
        super(Notification, self).__init__()
        ui_full_path = filetools.findFileInProduct('notification.ui')
        self.ui = uic.loadUi(ui_full_path, self)
        #self.model = QStandardItemModel()

        #self.listView.setModel(self.model)
        '''
        self.connect(self.listView.selectionModel(),  
                     QtCore.SIGNAL("selectionChanged(QItemSelection, QItemSelection)"),  
                     self.store_current_selection) 
        '''
        #self.show()
        '''
        self.listView.clicked.connect(self.item_clicked)
        self.minimized = True
        self.msg_signal.connect(self.msg_callback)
        '''
        self.setWindowFlags(QtCore.Qt.CustomizeWindowHint|QtCore.Qt.Tool|QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.X11BypassWindowManagerHint)
        self.vertical_adjust = 200
        self.max_cnt = 350
        size = self.geometry()
        self.width = size.width()
        self.height = size.height()
        '''
        self.not_over = True
        
        class mouseoverEvent(QtCore.QObject):
            def __init__(self, parent):
                super(mouseoverEvent, self).__init__(parent)
            def eventFilter(self, object, event):
                if event.type() == QtCore.QEvent.MouseMove:
                    #print "mousemove!"
                    self.not_over = False
                return False

        self.filter = mouseoverEvent(self)
        self.webView.installEventFilter(self.filter)
        '''
        
    def timeout(self):
        self.cnt += 1
        if self.cnt > self.max_cnt:
            self.ctimer.stop()
            self.hide()
        if self.cnt < 300:
            self.animate()
            if self.cnt < 2:
                print self.y
                self.move(self.x, self.y)
                self.show()
        else:
            if self.cnt < 301:
                milliseconds = 100
                self.ctimer.start(milliseconds)
            '''
            if self.not_over:
                self.disappear()
                self.not_over = True
            '''
            point = QtGui.QCursor.pos()
            if (point.x() > self.x) and (point.y() > self.y) and (point.x() < self.x + self.width) and (point.y() < self.y + self.height):
                #print 'over window'
                self.cnt -= 1
                pass
            else:
                #print point.x(), point.y(), self.x, self.y, self.width, self.height
                self.disappear()

    def noti(self, msg):
        self.noti_html('<body><div style="word-wrap: break-word;">notify:%s</div></body>'%(msg))
        
    def noti_html(self, msg):
        self.webView.setHtml(msg)
        self.ctimer = QtCore.QTimer()
        # constant timer
        QtCore.QObject.connect(self.ctimer, QtCore.SIGNAL("timeout()"), self.timeout)
        milliseconds = 1
        #Will trigger again and again. use self.ctimer.singleShot(milliseconds, callback) to get a single shot callback
        self.ctimer.start(milliseconds)
        self.init_x()
        self.cnt = 0
        self.f = 1
        
        
        
    #The following codes are copied from Pyqt-Notification- on github.
    
    def init_x(self):
        if True:#try:
            from ctypes import windll
            user32 = windll.user32
            #Get X coordinate of screen
            self.x = user32.GetSystemMetrics(0)
            self.y = user32.GetSystemMetrics(1) - self.vertical_adjust
        else:#except:
            cp = QtGui.QDesktopWidget().availableGeometry()
            self.x = cp.width()    
            self.y = cp.height() - self.vertical_adjust
    
    
    #Reduce opacity of the window
    def disappear(self):
        self.f -= 0.02
        self.setWindowOpacity(self.f)
        return
        
        
    #Move in animation
    def animate(self):
        #print '----------------------', self.x
        self.move(self.x, self.y)
        self.x -= 1
        return