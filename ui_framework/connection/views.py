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

# Create your views here.
@login_required
def index(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    c = {"user": request.user, "data_url": request.get_full_path().replace("pane/", "").replace("pane", ""), "diagram_id": uuid.uuid4()}
    c.update(csrf(request))
    return render_to_response('connection/connection_pane.html', c)

def save_diagram(request):
    pass
    
def create_diagram_obj(request):
    '''
    * Create diagram one connection after another. There will be a diagram uuid for all connections for this diagram.
    * UfsObj(ufs_url="diagram://uuid")
    '''
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    
    diag_uuid = data.get("diag_uuid", None)
    source = data.get("source", None)
    target = data.get("target", None)
    source_param = data.get("source_param", None)
    target_param = data.get("target_param", None)
    if (source is None) or (target is None) or (diag_uuid is None):
        raise "Invalid params"
    #Create diagram object
    #Find if the diagram object already exist
    if 0 == UfsObj.objects.filter(ufs_url = u"diagram://" + diag_uuid).count():
        obj = UfsObj(ufs_url = u"diagram://" + diag_uuid, uuid = unicode(diag_uuid), timestamp=timezone.now(), user = request.user)
        obj.save()
    else:
        obj = UfsObj.objects.get(ufs_url = u"diagram://" + diag_uuid)
    if source.isdigit():
        #source is digital so this processor has already been posted
        source_processor = Processor.objects.filter(pk=int(source))[0]
        #source_obj = 
    else:
        source_obj = UfsObj.objects.get(ufs_url = source)
        #Create processor
        source_processor = Processor(ufsobj = source_obj, param_descriptor = source_param)
        source_processor.save()
        
    if target.isdigit():
        #target is digital so this processor has already been posted
        target_processor = Processor.objects.filter(pk=int(target))[0]
    else:
        target_obj = UfsObj.objects.get(ufs_url = target)
        #Create processor
        target_processor = Processor(ufsobj = target_obj, param_descriptor = target_param)
        target_processor.save()
    #Add connections
    con = Connection(source = source_processor, target = target_processor, diagram = obj)
    con.save()
    return HttpResponse('{"source":%s, "target":%s}'%(source_processor.pk, target_processor.pk), mimetype="application/json")
    
import subprocess
from libs.console.ConsoleOutputCollector import execute_app

def parse_help(help_str):
    '''
    Internal function called by item_properties to parse app help
    '''
    param_start = False
    res = {}
    param_name = None
    description = None
    #res["log"] = ""
    for i in help_str.split("\n"):
        i = i.replace("\r", "")
        i = i.strip()
        if i == "":
            continue
        if param_start:
            if i[0:2] == "-h":
                param_name = "-h"
                res[param_name] = i.split(" ", 2)[1]

            if i[0:2] == "--":
                #It is a new param
                param_name = i.split(" ", 2)[0][2:]
                res[param_name] = i
                #res["log"] += param_name + "->" + i+","
            else:
                res[param_name] += " " + i
                #res["log"] += param_name + "->" + i +","
        if -1 != i.find("optional arguments:"):
            param_start = True
    #Remove default arguments
    del res["-h"]
    del res["startserver"]
    del res["session_id"]
    del res["diagram_id"]
    
    #Remove standard output
    for i in ["outputtube", "inputtube"]:
        if res.has_key(i):
            del res[i]
    return res

def item_properties(request):
    '''
    * Retrieve info from application help.
    '''
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    full_path = data.get("full_path", None)
    if full_path is None:
        return HttpResponse("{result: Error, no full_path provided}", mimetype="application/json")
    proc = execute_app(full_path, ["--help"])
    out = proc.communicate()[0]
    #print the output of the child process to stdout
    res = parse_help(out)
    
    #json_serializer = serializers.get_serializer("json")()
    #response =  json_serializer.serialize(res, ensure_ascii=False, indent=2, use_natural_keys=True)\
    response = json.dumps(res, sort_keys=True, indent=4)
    print response
    return HttpResponse(response, mimetype="application/json")
