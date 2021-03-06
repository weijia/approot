import json
import os
import sys
import time
import traceback
from ufs_django_conf import *

from connection.models import Processor, Connection
#from objsys.local_obj_tools import get_ufs_obj_from_ufs_url
from libtool.libtool import find_root
from libtool.filetools import collect_files_in_dir, get_app_name_from_full_path
from objsys.models import UfsObj
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from objsys.view_utils import get_ufs_obj_from_ufs_url
from services.sap.msg_service_sap import AutoRouteMsgService
from ufs_utils.misc import ensure_dir


gAutoStartDiagramTagName = "system:autostart"
gDiagramRootCollectionUuid = 'b4852a45-af7b-4a38-8025-15cf12212701'


def save_diagram_in_file_to_db(full_path):
    anonymous = User.objects.filter(pk=settings.ANONYMOUS_USER_ID)[0]
    file = open(full_path, 'r')
    data = json.load(file)
    diagram_uuid = data["diagram_id"]
    is_refresh_default_diagram_every_time = True
    if is_refresh_default_diagram_every_time:
        UfsObj.objects.filter(ufs_url=u"diagram://" + diagram_uuid, valid=True).delete()
        save_diagram(data, anonymous, False)
    else:
        diagram_obj_list = UfsObj.objects.filter(ufs_url=u"diagram://" + diagram_uuid, valid=True)
        if 0 == diagram_obj_list.count():
            save_diagram(data, anonymous, False)


class Diagram(object):
    def __init__(self, diagram_ufs_obj):
        self.diagram_ufs_obj = diagram_ufs_obj

    def get_info(self):
        tag_list = []
        for tag in self.diagram_ufs_obj.tags:
            tag_list.append(tag.name)

        processor_list = []
        for processor in Processor.objects.filter(diagram_obj=self.diagram_ufs_obj):
            processor_list.append(processor.ufsobj.ufs_url)

        return {"data": self.diagram_ufs_obj.ufs_url, "full_path": self.diagram_ufs_obj.ufs_url,
                "ufs_url": self.diagram_ufs_obj.ufs_url, "diagram_uuid": self.diagram_ufs_obj.uuid,
                "tags": tag_list, "description": "<br/>".join(processor_list)}


def save_all_diagram_from_predefined_folders():
    diagram_list = []
    diagram_file_list = []
    app_root_folder = find_root("approot")
    developing_diagram_relative_path = "libs/services/diagrams/"
    released_diagram_relative_path = "diagrams/"
    for sub_dir, ext in [(os.path.join(app_root_folder, developing_diagram_relative_path), ".json"),
                         (os.path.join(app_root_folder, released_diagram_relative_path), ".json")]:
        diagram_file_list.extend(collect_files_in_dir(sub_dir, ext))
    print diagram_file_list
    for full_path in diagram_file_list:
        save_diagram_in_file_to_db(full_path)
    return diagram_list


def save_diagram_str_to_file(processor_export_str):
    root_dir = find_root("approot")
    ensure_dir(os.path.join(root_dir, "../diagrams/"))
    dump_filename = os.path.join(root_dir, "../diagrams/" + str(time.time()) + ".json")
    f = open(dump_filename, "w")
    f.write(processor_export_str)
    f.close()
    return dump_filename


log = logging.getLogger(__name__)


def save_diagram(req_param, user, export_diagram=True):
    try:
        processor_list_in_req = req_param["processorList"]
        diagram_id = req_param["diagram_id"]
        auto_start = req_param.get("auto_start", False)
        info = ""
        connection_in_req_to_db_connection_mapping = {}
        for i in processor_list_in_req:
            info += i + ","
            diagram_obj = get_diagram_obj(diagram_id, user)

            if "params" in processor_list_in_req[i]:
                param = processor_list_in_req[i]["params"]
            else:
                param = {}
            param_str = json.dumps(param)

            #This object may be a script file object or a diagram object
            processor_ufs_obj = get_ufs_obj_from_ufs_url(processor_list_in_req[i]["ufs_url"])

            processor = create_processor(diagram_obj, processor_ufs_obj, param_str)

            for connection in processor_list_in_req[i]["inputs"]:
                #log.error("inputs: %d, %s" % (connection , str(connection_in_req_to_db_connection_mapping)))
                #connection is 0, 1 .... created in jquery diagram
                if not (connection in connection_in_req_to_db_connection_mapping):
                    conn = Connection()
                    #conn's uuid will be created automatically
                    conn.save()
                    #log.error("%s, %s" % (str(connection_in_req_to_db_connection_mapping), str(conn)))
                    connection_in_req_to_db_connection_mapping[connection] = conn
                else:
                    conn = connection_in_req_to_db_connection_mapping[connection]

                processor.inputs.add(conn)

            for connection in processor_list_in_req[i]["outputs"]:
                if not (connection in connection_in_req_to_db_connection_mapping):
                    conn = Connection()
                    conn.save()
                    connection_in_req_to_db_connection_mapping[connection] = conn
                else:
                    conn = connection_in_req_to_db_connection_mapping[connection]
                processor.outputs.add(conn)

            processor.save()

        #If there is no processor list, process standalone processors. Just to make it work currently
        if 0 == len(processor_list_in_req):
            standalone_processor_list = req_param["standaloneProcessor"]
            diagram_obj = get_diagram_obj(diagram_id, user)
            for processor_info, param_str in standalone_processor_list:
                processor_ufs_obj = get_ufs_obj_from_ufs_url(processor_info["ufs_url"])
                processor = create_processor(diagram_obj, processor_ufs_obj, param_str)

    except:
        traceback.print_exc()
        info += "processing: %s || %s" % (sys.exc_info()[0], sys.exc_info()[1])

    result_dict = {}

    if auto_start:
        diagram_obj.tags = gAutoStartDiagramTagName

    if export_diagram:
        processor_export_str = json.dumps(req_param, indent=4)
        result_dict['dumped'] = processor_export_str
        dump_filename = save_diagram_str_to_file(processor_export_str)
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


def update_diagram_list_from_database(diagram_list):
    for diagram_obj in UfsObj.objects.filter(ufs_url__startswith="diagram://").filter(valid=True):
        diagram_list.append(Diagram(diagram_obj))


def get_all_diagrams():
    diagram_list = save_all_diagram_from_predefined_folders()
    update_diagram_list_from_database(diagram_list)
    return diagram_list


def get_all_processors_for_diagram(diagram_id):
    diagram_obj = UfsObj.objects.get(uuid__exact=diagram_id)

    #The exclude filter removes state objects in Processor
    processors = Processor.objects.filter(diagram_obj__id=diagram_obj.pk).exclude(
        ufsobj__ufs_url=diagram_obj.ufs_url)
    return processors


def dispatch_to_processor(diagram_uuid, processor, base_msg):
    base_msg.update({"diagram": {"diagram_id": diagram_uuid, "processor_uuid": processor.uuid, }})
    param_dict = json.loads(processor.param_descriptor)
    base_msg.update(param_dict)
    target = get_app_name_from_full_path(processor.ufsobj.ufs_url)
    AutoRouteMsgService().send_to(target, base_msg)