import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread


class GuiService(beanstalkWorkingThread):
    def __init__ ( self, gui_factory = None, inputTubeName = None):
        super(GuiService, self).__init__(inputTubeName)
        #threading.Thread.__init__(self)
        self.gui_factory = gui_factory
    def processItem(self, job, item):
        self.gui_factory.trigger(item)
        job.delete()
        return False
    
    def gui_msg(self, s):
        self.put({"command":"notify", "msg": s})