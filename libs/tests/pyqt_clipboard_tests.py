from PyQt4 import QtCore, QtGui

app = QtGui.QApplication([])

data = QtCore.QMimeData()
#url = QtCore.QUrl.fromLocalFile('c:\\foo.file')
#data.setUrls([url])
data.setHtml('<h>hello</h>')
data.setText('hello')

app.clipboard().setMimeData(data)