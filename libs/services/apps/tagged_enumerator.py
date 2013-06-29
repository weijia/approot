import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread, beanstalkServiceApp
from libs.services.servicebase import service
from django.conf import settings
from ui_framework.objsys.models import UfsObj
from tagging.models import Tag, TaggedItem
import threading
import traceback

class TaggedEnumeratorThread(threading.Thread):
    def __init__ ( self, tag, output_tube_name):
        super(TaggedEnumeratorThread, self).__init__()
        self.tag = tag
        self.output_tube_name = output_tube_name
        
    def run(self):
        print 'Start enumerating:', self.tag
        try:
            obj_tag = Tag.objects.get(name=self.tag)
            #Use sorted query set instead of model so the object list order is constant
            objs = TaggedItem.objects.get_by_model(UfsObj.objects.order_by('timestamp'), obj_tag)
        except:
            print "No tagged item found"
            traceback.print_exc()
            return

        res = []
        for obj in objs:
            #path = obj.ufs_url.replace('file:///', '')
            path = obj.full_path
            output_service = beanstalkServiceApp(self.output_tube_name)
            output_service.addItem({"full_path": path, "fullpath": path})
            
            
class TaggedEnumerator(beanstalkServiceApp):
    def __init__(self, tube_name = None):
        super(TaggedEnumerator, self).__init__(tube_name)
        self.target_tube = {}

    def processItem(self, job, item):
        tag = item["tag"]
        output = item["output"]
        if (tag is None):
            print 'tag or output is none'
            print tag, output
        else:
            if item.has_key("output"):
                output = item["output"]
                if not (output is None):
                    if self.target_tube.has_key(tag):
                        #Already enumerating this tag
                        self.target_tube[tag].append(output)
                    else:
                        self.target_tube[tag] = [output]
                        
                    t = TaggedEnumeratorThread(tag, output)
                    if not self.is_processing_tube(tag+"::"+output):
                        self.add_work_thread(tag+"::"+output, t)
                        print 'Starting new working thread'
                        t.start()
            else:
                #Tagging notification add it directly to tube
                fullpath = item["fullpath"]
                for tube in self.target_tube[tag]:
                    output_service = beanstalkServiceApp(tube)
                    output_service.addItem({"fullpath": fullpath})

        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True
    
    
    
    
@service({
        "tag": "tag for enumerate",
        "output": "output tube name",
        #"blacklist": "blacklist for scanning, example: *.exe",
    })
def enum_obj_for_tag(is_server = None, args = {}):
    if is_server:
        s = TaggedEnumerator()
        s.startServer()
    else:
        s1 = TaggedEnumerator()
        s1.addItem({"command": "enumerate", "tag": args.tag, "output": args.output})
    
    
    
        
if __name__ == "__main__":
    enum_obj_for_tag()