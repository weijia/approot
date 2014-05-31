# -*- coding: gbk -*-
import logging
import sys
print sys.path
#There are 2 ufs_django_conf file in the codes. In exe, the file in root will be used. Otherwise, simple app
# use the local file located in service/simple_apps
from ufs_django_conf import *
from connection.models import Processor
from ufs_diagram.diagram_processing import get_all_processors_for_diagram, dispatch_to_processor
from services.pyro_service.pyro_simple_app_base import PyroSimpleAppBase

log = logging.getLogger(__name__)


class Distributor(PyroSimpleAppBase):
    def handle_req(self, msg):
        """
        {
            "diagram": {
                "diagram_id": "xxx-xxxxx-xxxxx",
                "processor_id": "xxx-xxxxx-xxxxx",
            },
            "is_all_tag": False,
            "tag": "git_repo"
        })
        """
        diagram_id = msg["diagram"]["diagram_id"]
        processors = get_all_processors_for_diagram(diagram_id)
        for processor in processors:
            if processor.uuid == msg["diagram"]["processor_uuid"]:
                try:
                    connection = processor.outputs.all()[0]
                except IndexError:
                    log.error("No output processor found for %s on connection: %s" % (processor, connection))
                target_processor = Processor.objects.filter(inputs=connection)[0]
                dispatch_to_processor(diagram_id, target_processor, msg)

'''
def start_diagrams():
    time.sleep(1)
    for diagram in get_all_diagrams():
        diagram_uuid = diagram.get_info()["diagram_uuid"]
        processors_for_diagram = get_all_processors_for_diagram(diagram_uuid)
        for processor in processors_for_diagram:
            input_count = processor.inputs.count()
            if 0 == input_count:
                dispatch_to_processor(diagram_uuid, processor, {})
'''


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    s = Distributor()
    #thread.start_new_thread(start_diagrams, ())
    print "Before start service"
    s.start_service()
    print "After start service"
