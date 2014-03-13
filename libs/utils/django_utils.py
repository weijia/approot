import json
import mimetypes
from django.http import HttpResponse
import os
from django.core.servers.basehttp import FileWrapper
from django.utils.http import urlquote


def retrieve_param(request):
    if request.method == "GET":
        data = request.GET
    else:
        data = request.POST
    return data


def return_file_data(the_file):
    filename = os.path.basename(unicode(the_file))
    response = HttpResponse(FileWrapper(open(the_file, 'rb')),
                            content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = u"attachment; filename=%s" % urlquote(filename)
    return response


def get_content_item_list_in_tastypie_format(item_list):
    res = []
    for item in item_list:
        res.append(item.get_info())
    response = json.dumps({"objects": res, "meta": {"next": None}}, sort_keys=True, indent=4)
    return HttpResponse(response, mimetype="application/json")


def get_list_in_json(item_list):
    res = []
    for item in item_list:
        res.append(item.get_info())
    response = json.dumps(res, sort_keys=True, indent=4)
    return HttpResponse(response, mimetype="application/json")


def get_json_resp(res):
    response = json.dumps(res, sort_keys=True, indent=4)
    return HttpResponse(response, mimetype="application/json")