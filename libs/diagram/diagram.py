import json
import os
import sys
import time
import traceback
from libs.utils.obj_tools import get_ufs_obj_from_ufs_url
import libsys
from libs.utils import filetools as file_tools

from ui_framework.connection.models import Processor, Connection
#from ui_framework.objsys.local_obj_tools import get_ufs_obj_from_ufs_url
from ui_framework.objsys.models import UfsObj
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


gAutoStartDiagramTagName = "system:autostart"
gDiagramRootCollectionUuid = 'b4852a45-af7b-4a38-8025-15cf12212701'



def save_diagram_to_db(full_path):
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


def save_all_diagram_from_predefined_folders():
    diagram_list = []
    diagram_file_list = []
    for sub_dir, ext in [("/libs/services/apps/diagrams/", ".json"), ("/diagrams/", ".json")]:
        diagram_file_list.extend(file_tools.collect_files_in_dir(sub_dir, ext))
    print diagram_file_list
    for full_path in diagram_file_list:
        save_diagram_to_db(full_path)
    return diagram_list


def save_diagram(req_param, user, export_diagram=True):
    try:
        processor_list = req_param["processorList"]
        diagram_id = req_param["diagram_id"]
        auto_start = req_param.get("auto_start", False)
        info = ""
        connection_uuid_list = {}
        for i in processor_list:
            info += i + ","
            diagram_obj = get_diagram_obj(diagram_id, user)

            if "params" in processor_list[i]:
                param_str = processor_list[i]["params"]
            else:
                param = {}
                param_str = json.dumps(param)

            #This object may be a script file object or a diagram object
            obj = get_ufs_obj_from_ufs_url(processor_list[i]["ufs_url"])

            processor = create_processor(diagram_obj, obj, param_str)

            for connection in processor_list[i]["inputs"]:
                #connection is 0, 1 .... created in jquery diagram
                if not connection_uuid_list.has_key(connection):
                    conn = Connection()
                    #conn's uuid will be created automatically
                    conn.save()
                    connection_uuid_list[connection] = conn
                else:
                    conn = connection_uuid_list[connection]
                processor.inputs.add(conn)

            for connection in processor_list[i]["outputs"]:
                if not (connection in connection_uuid_list):
                    conn = Connection()
                    conn.save()
                    connection_uuid_list[connection] = conn
                else:
                    conn = connection_uuid_list[connection]
                processor.outputs.add(conn)

            processor.save()

        #If there is no processor list, process standalone processors. Just to make it work currently
        if 0 == len(processor_list):
            standalone_processor_list = req_param["standaloneProcessor"]
            diagram_obj = get_diagram_obj(diagram_id, user)
            for processor_info, param_str in standalone_processor_list:
                obj = get_ufs_obj_from_ufs_url(processor_info["ufs_url"])
                processor = create_processor(diagram_obj, obj, param_str)

    except:
        traceback.print_exc()
        info += "processing: %s || %s" % (sys.exc_info()[0], sys.exc_info()[1])

    result_dict = {}

    if auto_start:
        diagram_obj.tags = gAutoStartDiagramTagName

    if export_diagram:
        processor_export_str = json.dumps(req_param, indent=4)
        result_dict['dumped'] = processor_export_str
        root_dir = libsys.get_root_dir()

        try:
            os.mkdir(os.path.join(root_dir, "../diagrams/"))
        except:
            #Maybe it already exists.
            pass
        dump_filename = os.path.join(root_dir, "../diagrams/" + str(time.time()) + ".json")
        f = open(dump_filename, "w")
        f.write(processor_export_str)
        f.close()
        result_dict['dump_file'] = dump_filename

    result_dict['message'] = info
    result_dict['diagram_id'] = diagram_id
    return result_dict


def get_diagram_obj(diagram_id, user):
    #Find if the diagram object already exist
    if 0 == UfsObj.objects.filter(ufs_url=u"diagram://" + diagram_id).count():
        diagram_obj = UfsObj(ufs_url=u"diagram://" + diagram_id, uuid=unicode(diagram_id),
                             timestamp=timezone.now(), user=user)
        diagram_obj.save()
    else:
        diagram_obj = UfsObj.objects.get(ufs_url=u"diagram://" + diagram_id)
    return diagram_obj


def create_processor(diagram_obj, obj, param_str):
    #Create processor
    processor = Processor(ufsobj=obj, diagram_obj=diagram_obj, param_descriptor=param_str)
    processor.save()
    return processor