# -*- coding: gbk -*-
import logging
from ufs_django_conf import *
from connection.models import Processor
from diagram.diagram import get_all_processors_for_diagram, dispatch_to_processor
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
            if processor.ufsobj.uuid == msg["diagram"]["processor_id"]:
                try:
                    connection = processor.outputs.all()[0]
                except IndexError:
                    print processor, connection
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
    s.start_service()
