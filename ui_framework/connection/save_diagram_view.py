from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
import uuid
from django.utils import timezone
from models import Connection, Processor
from ui_framework.objsys.models import UfsObj
from django.http import HttpResponse
from django.core import serializers
import libs.utils.simplejson as json
from django.contrib.auth.decorators import login_required
import time
import json
import traceback
import sys
import libsys
import os

def save_diagram(req_param, user, export_diagram = True):
    try:
        processor_list = req_param["processorList"]
        diagram_id = req_param["diagram_id"]
        info = ""
        connection_uuid_list = {}
        for i in processor_list:
            info += i + ","
            #Find if the diagram object already exist
            if 0 == UfsObj.objects.filter(ufs_url = u"diagram://" + diagram_id).count():
                diagram_obj = UfsObj(ufs_url = u"diagram://" + diagram_id, uuid = unicode(diagram_id), timestamp=timezone.now(), user = user)
                diagram_obj.save()
            else:
                diagram_obj = UfsObj.objects.get(ufs_url = u"diagram://" + diagram_id)
                
            if processor_list[i].has_key("params"):
                param_str = processor_list[i]["params"]
            else:
                param = {}
                param_str = json.dumps(param)
            #This object may be a script file object or a diagram object
            obj = UfsObj.objects.get(ufs_url = processor_list[i]["ufs_url"])
            

            #Create processor
            processor = Processor(ufsobj = obj, diagram_obj= diagram_obj, param_descriptor = param_str)
            processor.save()
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
                if not connection_uuid_list.has_key(connection):
                    conn = Connection()
                    conn.save()
                    connection_uuid_list[connection] = conn
                else:
                    conn = connection_uuid_list[connection]
                processor.outputs.add(conn)
                    
            processor.save()
                    
    except:
        traceback.print_exc()
        info += "processing: %s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        
    result_dict = {}

    if export_diagram:
        processor_export_str = json.dumps(req_param, indent=4)
        result_dict['dumpped'] = processor_export_str
        root_dir = libsys.get_root_dir()

        try:
            os.mkdir(os.path.join(root_dir, "../diagrams/"))
        except:
            #Maybe it already exists.
            pass
        dump_filename = os.path.join(root_dir, "../diagrams/"+str(time.time())+".json")
        f = open(dump_filename, "w")
        f.write(processor_export_str)
        f.close()
        result_dict['dump_file'] = dump_filename
        
    result_dict['message']=info
    result_dict['diagram_id'] = diagram_id
    return result_dict

# Create your views here.
def handle_save_diagram(request):
    '''
    * Save diagram,
    {"diagram_id":"65d6db19-fc45-471c-818c-97e52dd3de20",
        "processorList":{"jsPlumb_1_11":
                        {"inputs":[],"outputs":[0],
                            "script_url":"file:///D:/codes/mine/env/codes/ufs_django/approot/libs/services/apps/tagged_enumerator.py"
                        },
                     "jsPlumb_1_6":
                        {"inputs":[0],"outputs":[],"script_url":"file:///D:/codes/mine/env/codes/ufs_django/approot/libs/services/apps/git_puller.py"
                        }
                    }
    }:
    '''

    
    result_dict = {}
    handler_error = 'Data log save success'
    try:
        if request.method == 'POST':
            req_dict = json.loads(request.raw_post_data)
            print req_dict
            result_dict = save_diagram(req_dict, request.user)
        else:
            raise "Not post"
    except:
        traceback.print_exc()
        handler_error += "%s || %s" % (sys.exc_info()[0], sys.exc_info()[1])
        
    result_dict['message'] += handler_error
    result_dict['create_at']=str(time.ctime())

    jsonstr=json.dumps(result_dict, indent=4)
    return HttpResponse(jsonstr)
