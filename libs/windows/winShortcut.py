#Copied from http://bytes.com/topic/python/answers/711949-resolving-windows-shortcut-url

from win32com.shell import shell
import pythoncom
import os, sys

class PyShortcut(object):
    def __init__(self):
        self._base = pythoncom.CoCreateInstance(shell.CLSID_ShellLink, 
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IShellLink)

    def load(self, filename):
        self._base.QueryInterface(pythoncom.IID_IPersistFile).Load(filename)

    def save(self, filename):
        self._base.QueryInterface(pythoncom.IID_IPersistFile).Save(filename, 0)

    def __getattr__(self, name):
        if name != "_base":
            return getattr(self._base, name)


if __name__=="__main__":
    lnk = PyShortcut()
    lnk.load("E:\\apps\\mongodb-win32-i386-1.8.1\\bin\\Shortcut to mongod.exe.lnk")
    print "Location:", lnk.GetPath(shell.SLGP_RAWPATH)[0]
    print "arg:", lnk.GetArguments()