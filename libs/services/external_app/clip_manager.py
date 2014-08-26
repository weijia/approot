from PyQt4 import QtCore
from clip_manager_ui import Ui_MainWindow
import sys
from PyQt4.QtGui import QApplication, QDialog, QMainWindow, QFileDialog


class ClipManagerApp(object):
    def __init__(self):
        app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)

        self.window.connect(self.ui.action, QtCore.SIGNAL('triggered()'), self.on_open)
        self.window.connect(self.ui.action_3, QtCore.SIGNAL('triggered()'), self.on_exit)

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


def main():
    c = ClipManagerApp()


if __name__ == "__main__":
    main()