from django.shortcuts import render_to_response, redirect
from django.core.context_processors import csrf
from ufs_diagram.diagram_processing import save_diagram

from django.http import HttpResponse
#from django.core import serializers
from django.contrib.auth.decorators import login_required
import time
import json
import traceback
import sys


# Create your views here.
def handle_save_diagram(request):
    """
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
    """

    result_dict = {"message": ""}
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
    result_dict['create_at'] = str(time.ctime())

    json_str = json.dumps(result_dict, indent=4)
    return HttpResponse(json_str)
