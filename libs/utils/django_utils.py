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