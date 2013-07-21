import json
import os
import libsys
from ui_framework.connection.models import Processor
from ui_framework.connection.save_diagram_view import save_diagram
from ui_framework.objsys.models import UfsObj
from django.contrib.auth.models import User
from django.conf import settings


def import_diagram(full_path):
    anonymous = User.objects.filter(pk=settings.ANONYMOUS_USER_ID)[0]
    file = open(full_path, 'r')
    data = json.load(file)
    diagram_id = data["diagram_id"]
    diag_obj_list = UfsObj.objects.filter(ufs_url = u"diagram://" + diagram_id)
    if 0 == diag_obj_list.count():
        save_diagram(data, anonymous, False)


class Diagram(object):
    def __init__(self, diagram_obj):
        self.diagram_obj = diagram_obj

    def get_info(self):
        tag_list = []
        for tag in self.diagram_obj.tags:
            tag_list.append(tag.name)

        processor_list = []
        for processor in Processor.objects.filter(diagram_obj=self.diagram_obj):
            processor_list.append(processor.ufsobj.ufs_url)

        return {"data": self.diagram_obj.ufs_url, "full_path": self.diagram_obj.ufs_url,
                "ufs_url": self.diagram_obj.ufs_url, "tags": tag_list, "description": "<br/>".join(processor_list)}