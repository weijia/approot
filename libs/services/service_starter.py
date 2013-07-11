import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread
from libs.services.svc_base.gui_service import GuiService
import urllib
from django.conf import settings
from ui_framework.objsys.models import UfsObj, CollectionItem
#from tagging.models import Tag, TaggedItem, DoesNotExist
import os
import libs.utils.simplejson as json
from ui_framework.connection.models import Connection, Processor
import libs.utils.filetools as file_tools
import time


def start_app(app_path, param_dict):
    param = []
    for i in param_dict:
        param.append('--%s'%(i))
        param.append('%s'%(param_dict[i]))
    '''
    if not os.path.exists(path):
        filename = os.path.basename(path)
        path = os.path.join(os.getcwd(), 'libs/services/apps/'+filename)
    '''
    print app_path
    app_path = os.path.basename(app_path)
    print "base:", app_path
    app_path = app_path.split(".")[0]
    app_path = file_tools.findAppInProduct(app_path)
    print "found:", app_path
    if os.path.exists(app_path):
        gui_service = GuiService()
        gui_service.addItem({"command": "Launch", "path": app_path, "param": param})
        #print {"command": "Launch", "path": path, "param": param}

diagram_root = 'b4852a45-af7b-4a38-8025-15cf12212701'

def service_starter():
    
    
    #Get all diagrams
    diagram_lists = CollectionItem.objects.filter(uuid=diagram_root)
    
    created_processor = []
    for coll_item in diagram_lists:
        #print 'starting diagram:', coll_item.obj.ufs_url
        start_diagram(coll_item.obj)


def start_diagram(diagram_obj, connection_prefix = u''):
    """
    * Start diagram

    for processor in diagram:
        if processor is diagram:
            start diagram(processor.params)
        else:
            start processor(processor.params)
    """
    print diagram_obj
    session_id = time.time()
    
    for processor in Processor.objects.filter(diagram_obj = diagram_obj):
        print 'processing processor', processor.ufsobj.ufs_url
        if "diagram://" in processor.ufsobj.ufs_url:
            #It is a diagram or it is the processor for the diagram. We need to identify the processor object for this diagram
            if diagram_obj != processor.ufsobj:
                start_diagram(sub_diagram_obj, processor.ufsobj.uuid)
            else:
                continue
        else:
            #It is a processor, so ufs url pointer to a script file object
            #print "starting processor: ", processor.ufsobj.ufs_url
            param = json.loads(processor.param_descriptor)
            if 0 != processor.inputs.count():
                param['input'] = connection_prefix + u"." + processor.inputs.all()[0].connection_uuid
            if 0 != processor.outputs.count():
                param['output'] = connection_prefix + u"." + processor.outputs.all()[0].connection_uuid
            processor_path = processor.ufsobj.ufs_url.replace("file:///", "")
            param['session_id'] = session_id
            param['diagram_id'] = diagram_obj.uuid
            start_app(processor_path, param)
        
        
if __name__ == "__main__":
    print 'starting diagrams --------------------------------------'
    service_starter()