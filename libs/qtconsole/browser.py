from PyQtConsoleOutputWnd import ToggleMaxMin, MinimizeOnClose
from PyQt4.QtWebKit import *

class Browser(QWebView, ToggleMaxMin, MinimizeOnClose):
    pass