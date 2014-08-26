from PyQt4 import QtCore
from clip_manager_ui import Ui_MainWindow
import sys
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog
from PyQt4 import Qsci

class ClipManagerApp(object):
    def __init__(self):
        app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)

        self.window.connect(self.ui.action, QtCore.SIGNAL('triggered()'), self.on_open)
        self.window.connect(self.ui.action_3, QtCore.SIGNAL('triggered()'), self.on_exit)
        self.window.connect(self.ui.action_4, QtCore.SIGNAL('triggered()'), self.on_execute)

        self.ui.textEdit.setLexer(Qsci.QsciLexerPython())

        self.ui.textEdit.setText("""#y=x
##or
#yl = []
#for i in xl:
#    yl.append(i+"i")
"""
        )
        self.window.show()
        sys.exit(app.exec_())

    def on_open(self):
        fname = QFileDialog.getOpenFileName(self.window, 'Open file',
                                            '/')
        if fname != "":
            f = open(fname, 'r')

            with f:
                data = f.read()
                self.ui.textEdit.setText(data)

    def on_exit(self):
        self.window.close()

    def on_execute(self):
        script_text = str(self.ui.textEdit.text())
        # print 'script is:',script_text
        source_text = str(self.ui.textEdit_2.text())
        source_text = source_text.replace('\r', '')
        xl = source_text.split('\n')
        #Set source text to x so script can use x as source text as well
        x = source_text
        y = None
        t = None
        exec script_text
        #print y
        if y is None:
            y = '\n'.join(yl)
            #print y
        self.ui.textEdit_3.setText(y)

        """
        if self.autoTransformFlag:
            if (t is None) or t:
                print 'setting text to %s' % y
                type = self.combo.child.get_text()
                print 'current type is:', type
                self.setClipboardData(type, y)
        """


def main():
    c = ClipManagerApp()


if __name__ == "__main__":
    main()