import libsys
from libs.services.svc_base.launcher_interface import Launcher
from libs.diagram.diagram import save_all_diagram_from_predefined_folders, gAutoStartDiagramTagName, \
    gDiagramRootCollectionUuid
from tagging.models import TaggedItem
#from libs.services.svc_base.beanstalkd_interface import beanstalkWorkingThread
from django.conf import settings
from ui_framework.objsys.models import UfsObj, CollectionItem
#from tagging.models import Tag, TaggedItem, DoesNotExist
#import libs.utils.simplejson as json
from ui_framework.connection.models import Processor
import json


def service_starter():
    #Get all diagrams
    diagram_lists = CollectionItem.objects.filter(uuid=gDiagramRootCollectionUuid)

    created_processor = []
    for coll_item in diagram_lists:
        #print 'starting diagram:', coll_item.obj.ufs_url
        start_diagram(coll_item.obj)


def start_diagram_by_tag():
    obj_list = TaggedItem.objects.get_by_model(UfsObj.objects.order_by('timestamp'), gAutoStartDiagramTagName)
    for obj in obj_list:
        if "diagram://" in obj.ufs_url:
            start_diagram(obj)


def start_diagram(diagram_obj, connection_prefix=u''):
    """
    * Start diagram

    for processor in diagram:
        if processor is diagram:
            start diagram(processor.params)
        else:
            start processor(processor.params)
    """
    log_str = str(diagram_obj)
    print diagram_obj
    #session_id = time.time()

    for processor in Processor.objects.filter(diagram_obj=diagram_obj):
        print 'processing processor', processor.ufsobj.ufs_url
        log_str += processor.ufsobj.ufs_url + "\n"
        if "diagram://" in processor.ufsobj.ufs_url:
            #It is a diagram or it is the processor for the diagram. We need to identify the processor object for this diagram
            if diagram_obj != processor.ufsobj:
                start_diagram(sub_diagram_obj, processor.ufsobj.uuid)
            else:
                continue
        else:
            #It is a processor, so ufs url pointer to a script file object
            #print "starting processor: ", processor.ufsobj.ufs_url
            try:
                param = json.loads(processor.param_descriptor)
            except:
                param = {}
            if 0 != processor.inputs.count():
                param['input'] = connection_prefix + u"." + processor.inputs.all()[0].connection_uuid
            if 0 != processor.outputs.count():
                param['output'] = connection_prefix + u"." + processor.outputs.all()[0].connection_uuid
            processor_ufs_url = processor.ufsobj.ufs_url
            #param['session_id'] = session_id
            param['diagram_id'] = diagram_obj.uuid
            log_str += "starting:" + processor_ufs_url + "+" + str(param)
            log_str += Launcher().start_app_with_same_filename_with_param_dict(processor_ufs_url, param)
    return log_str


if __name__ == "__main__":
    print 'starting diagrams --------------------------------------'
    save_all_diagram_from_predefined_folders()
    start_diagram_by_tag()