import os
import subprocess
import threading
from win32process import CREATE_NO_WINDOW
import sys
import libsys
import _subprocess

__author__ = 'Richard'


class CrossPlatformProcessMgrBase(object): pass


class ConsoleReaderThread(threading.Thread):
    def __init__(self, target, fileD, app_name='unknown', output_to_console=False, logFilePath=None):
        self.target = target
        threading.Thread.__init__(self)
        self.quitFlag = False
        self.fileD = fileD
        self.app_name = app_name
        self.output_to_console = output_to_console
        self.logFilePath = logFilePath

    def write_file_if_needed(self, err):
        if not (self.output_file is None):
            try:
                self.output_file.write(err)
            except:
                pass

    def run(self):
        print 'running----------------------'
        if not (self.logFilePath is None):
            self.output_file = open(self.logFilePath, "w")
        else:
            self.output_file = None
        while not self.quitFlag:
            #print 'before readline'
            err = self.fileD.readline()
            try:
                err = err.decode("gbk")
            except:
                try:
                    err = err.decode("utf8")
                except:
                    pass
                #print 'after readline'
            if err == '':
                #print 'err is empty'
                self.quit()
            if err is None:
                self.quit()
                #print 'quit'
                break
            if self.output_to_console:
                #print 'got output:', self.app_name, ':  ',err
                pass
            self.write_file_if_needed(err)
            self.target.on_updated(err)
        if not (self.output_file is None):
            self.output_file.close()
        print 'quitting run: ', self.app_name

    def quit(self):
        self.quitFlag = True


class ProcessMgrForWin32(CrossPlatformProcessMgrBase):
    def wait_for_complete_without_console(self, path_and_param_list, working_dir):
        '''
        #print subprocess.PIPE
        p = subprocess.Popen(path_and_param_list, cwd=working_dir, stdout=sys.stdout,
                             stderr=sys.stderr, bufsize=0, shell=True,
                             creationflags=CREATE_NO_WINDOW).wait()
        '''
        #startupinfo = subprocess.STARTUPINFO()
        #startupinfo.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
        #p = subprocess.call(" ".join(path_and_param_list), cwd=working_dir, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = subprocess.Popen(" ".join(path_and_param_list), cwd=working_dir, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=0, creationflags=CREATE_NO_WINDOW)
        """
        fd = p.stderr.fileno()
        unbuffered_stderr = os.fdopen(os.dup(fd), 'rU', 0)
        os.close(fd)
        """
        err = ConsoleReaderThread(self, p.stderr)
        err.start()
        out = ConsoleReaderThread(self, p.stdout)
        out.start()
        err.join()
        out.join()

    def on_updated(self, line):
        print line,
        sys.stdout.flush()


gProcessMgr = ProcessMgrForWin32

