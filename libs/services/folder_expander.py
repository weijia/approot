import libsys
from libs.services.beanstalkdServices.beanstalkServiceBaseV2 import beanstalkWorkingThread, beanstalkServiceApp
from libs.services.servicebase import service
from django.conf import settings
from objsys.models import UfsObj
from tagging.models import Tag, TaggedItem

class FolderExpanderThread(beanstalkWorkingThread):
    def __init__ ( self, input_tube_name, output_tube_name):
        super(FolderExpanderThread, self).__init__(input_tube_name)
        self.output_tube_name = output_tube_name
        self.output_tube = beanstalkServiceApp(output_tube_name)
        
    def processItem(self, job, item):
        if not os.path.isdir(item["fullpath"]):
            self.output_tube.addItem({"fullpath": item["fullpath"]})
        else:
            for i in os.walk(item["fullpath"]):
                #This will be set to True by external app
                if self.quit_flag:
                    break
                for j in i[2]:
                    info(j)
                    fullpath = transform.transformDirToInternal(os.path.join(i[0], j))
                    self.output_tube.addItem({"fullpath": fullPath})

        job.delete()
        return False#Return False if we do not need to put the item back to tube

            
            
class FolderExpander(beanstalkServiceApp):
    def processItem(self, job, item):
        input = item["input"]
        output = item["output"]
        t = FolderExpanderThread(input, output)
        if self.is_processing_tube(tag+"::"+output):
            job.delete()
            return False
        self.add_work_thread(tag+"::"+output, t)
        print 'Starting new working thread'
        t.start()
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True
    
    
    
    
@service({
        "input": "input tube name",
        "output": "output tube name",
        #"blacklist": "blacklist for scanning, example: *.exe",
    })
def expand_folder(is_server = None, args = {}):
    if is_server:
        s = FolderExpander()
        s.startServer()
    else:
        s1 = FolderExpander()
        s1.addItem({"command": "expand", "input": args.input, "output": args.output})
    
    
    
        
if __name__ == "__main__":
    enum_obj_for_tag()