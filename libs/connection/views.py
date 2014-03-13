import os
import uuid
import json

from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from diagram.diagram import Diagram, save_all_diagram_from_predefined_folders
#from libs.services.svc_base.msg_based_service_mgr import gMsgBasedServiceManagerMsgQName
#from libs.services.svc_base.msg_service import MsgQ
#from libs.services.svc_base.service_starter import start_diagram
from libtool import find_root_path
from libtool.filetools import find_callable_in_app_framework, collect_files_in_dir

from objsys.models import UfsObj
from django.http import HttpResponse

#import libs.utils.simplejson as json
from django.contrib.auth.decorators import login_required
from platform_related.executor import execute_app
from services.svc_base.service_starter import start_diagram
from utils.django_utils import retrieve_param, get_content_item_list_in_json_rest, get_list_in_json, get_json_resp

# Create your views here.
from objsys.view_utils import get_ufs_obj_from_ufs_url, get_ufs_obj_from_full_path


@login_required
def index(request):
    data = retrieve_param(request)
    c = {"user": request.user, "data_url": request.get_full_path().replace("pane/", "").replace("pane", ""),
         "diagram_id": uuid.uuid4()}
    c.update(csrf(request))
    return render_to_response('connection/connection_pane.html', c)


def parse_help(help_str):
    """
    Internal function called by item_properties to parse app help
    """
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
    for i in ["outputtube", "inputtube", "input_msg_queue", "output_msg_queue"]:
        if i in res:
            del res[i]
    return res


def item_properties(request):
    """
    * Retrieve info from application help.
    """
    data = retrieve_param(request)
    full_path = data.get("full_path", None)
    if full_path is None:
        return HttpResponse("{result: Error, no full_path provided}", mimetype="application/json")
    if "scache.bat" in full_path:
        #Ignore scache
        res = {}
    else:
        proc = execute_app(full_path, ["--help"])
        out = proc.communicate()[0]
        #print the output of the child process to stdout
        #print out
        res = parse_help(out)

        #json_serializer = serializers.get_serializer("json")()
        #response =  json_serializer.serialize(res, ensure_ascii=False, indent=2, use_natural_keys=True)\
        response = json.dumps(res, sort_keys=True, indent=4)
        #print response
    return HttpResponse(response, mimetype="application/json")


class App(object):
    """
    Can not be called directly
    """
    def get_info(self):
        ufs_obj = get_ufs_obj_from_full_path(self.app_full_path)
        return {"data": self.app_name, "full_path": ufs_obj.full_path, "ufs_url": ufs_obj.ufs_url}


class FullPathApp(App):
    def __init__(self, app_full_path):
        self.app_full_path = app_full_path
        self.app_name = os.path.basename(self.app_full_path).split(".")[0]


class NamedApp(App):
    def __init__(self, app_name):
        self.app_name = app_name
        self.app_full_path = app_path = find_callable_in_app_framework(self.app_name)
        if app_path is None:
            raise "Obj not exists"


gIgnoreAppList = ["root.exe", "__init__.py", "libsys.py",
                  "postgresql.bat",
                  "postgresql_stop.bat",
                  "start_ext.bat",
                  "start_ext_app.bat",
                  "startBeanstalkd.bat",
                  #"mongodb.bat"
                  #"syncdb.bat",
                  #"tornado.bat",
                  #"tornado_app.bat",
                  #"runserver.bat",
                  #"makedoc.bat"
                  #"activate.bat"
                  #"activate_app.bat",
                  #"cmd_prompt.bat"
]


def get_service_apps(request):
    app_path_list = []
    #for app_name in gDefaultServices:
    #    app_list.append(NamedApp(app_name))
    #Add root folder .exe, (used for built apps)
    root_dir = find_root_path(__file__, "approot")
    for sub_dir, ext in [("/", ".exe"), ("libs/services/simple_app/", ".py"),
                         ("libs/services/external_app/", ".bat"),
                         ("/external/", ".bat")]:
        sub_dir_full_path = os.path.join(root_dir, sub_dir)
        app_path_list.extend(collect_files_in_dir(sub_dir_full_path, ext, gIgnoreAppList))
    app_list = []
    for full_path in app_path_list:
        app_list.append(FullPathApp(full_path))
    return get_list_in_json(app_list)


def get_diagrams(request):
    diagram_list = save_all_diagram_from_predefined_folders()

    for diagram_obj in UfsObj.objects.filter(ufs_url__startswith="diagram://"):
        diagram_list.append(Diagram(diagram_obj))
    return get_content_item_list_in_json_rest(diagram_list)


def handle_start_diagram_req(request):
    data = retrieve_param(request)
    diagram_obj = get_ufs_obj_from_ufs_url(data["ufs_url"])
    log_str = start_diagram(diagram_obj)
    res = {"log": log_str}
    return get_json_resp(res)


def handle_stop_diagram_req(request):
    data = retrieve_param(request)
    diagram_obj = get_ufs_obj_from_ufs_url(data["ufs_url"])
    """
    MsgQ(gMsgBasedServiceManagerMsgQName).send_cmd({"cmd": "broadcast_cmd",
                                                    "session_id": os.environ["ufs_console_mgr_session_id"],
                                                    "msg": {"cmd": "stop_diagram",
                                                            "diagram_id": diagram_obj.uuid,
                                                            "session_id": os.environ["ufs_console_mgr_session_id"]}
    })
    """

    res = {"result": data["ufs_url"] + ":" + diagram_obj.uuid + " stop diagram message sent"}
    response = json.dumps(res, sort_keys=True, indent=4)
    return HttpResponse(response, mimetype="application/json")