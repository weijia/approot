import libsys
from diagram.diagram import save_all_diagram_from_predefined_folders, gAutoStartDiagramTagName, \
    gDiagramRootCollectionUuid, get_all_processors_for_diagram
from iconizer.pyro_launcher import Launcher
from tagging.models import TaggedItem

from django.conf import settings
from collection_management.models import CollectionItem
from objsys.models import UfsObj
from services.simple_app.distributor import dispatch_to_processor


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
    diagram_uuid = diagram_obj.uuid
    res = ""
    processors_for_diagram = get_all_processors_for_diagram(diagram_uuid)
    res += str(processors_for_diagram)
    for processor in processors_for_diagram:
        input_count = processor.inputs.count()
        if 0 == input_count:
            dispatch_to_processor(diagram_uuid, processor, {})
    return res


if __name__ == "__main__":
    print 'starting diagrams --------------------------------------'
    save_all_diagram_from_predefined_folders()
    start_diagram_by_tag()