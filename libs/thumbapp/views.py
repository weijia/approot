import os
import mimetypes
from django.core.servers.basehttp import FileWrapper
from thumb.thumbInterface import get_thumb
from libs.obj_related.local_obj import LocalObj
from libs.thumbapp.qrcode_image import get_qr_code
from libs.utils.django_utils import retrieve_param

import libsys
from django.http import HttpResponse
from ui_framework.objsys.models import UfsObj, get_ufs_obj_from_full_path
from libs.utils.transform import transformDirToInternal
from models import ThumbCache
import libs.utils.objTools as objtools
import uuid
from django.utils import timezone
from libs.utils.misc import ensureDir as ensure_dir
from django.shortcuts import render_to_response, redirect
from django.utils.http import urlquote
from libs.logsys.logSys import *
from django.template import RequestContext


from urllib import unquote


def get_thumb_file(target_file):
    full_path = transformDirToInternal(target_file)
    if not os.path.exists(full_path):
        the_file = '/static/image/icons/file-broken-icon.png'
    else:
        obj = get_ufs_obj_from_full_path(full_path)
        thumb_list = ThumbCache.objects.filter(obj=obj)

        if 0 == thumb_list.count():

            #Thumb not generated, generate it
            target_dir = os.path.join(libsys.get_root_dir(), "../thumb")
            ensure_dir(target_dir)

            the_file = get_thumb(target_file, target_dir)

            if not (the_file is None):
                ThumbCache(obj=obj, thumb_full_path=the_file).save()

        else:
            the_file = thumb_list[0].thumb_full_path

        if the_file is None:
            the_file = get_icon(full_path, obj.get_type())
            raise "No thumb"
    return the_file


def get_icon(full_path, file_type=None):
    if os.path.isdir(full_path):
        return '/static/image/icons/folder-images-icon.png'

    if file_type is None:
        file_type = LocalObj(full_path).get_type()

    cl(full_path, 'file type is:', file_type)

    if 'Zip archive data' in file_type:
        ext = full_path.split('.')[-1]
        for ext_prefix in ["xls", "doc", "ppt"]:
            if ext_prefix+"x" in ext:
                return '/static/image/icons/online/512px/' + ext_prefix + '.png'

    ext_icons = ['html', 'xml', 'pdf']
    for i in ext_icons:
        if i in file_type.lower().split(" "):
            return '/static/image/icons/online/512px/' + i + '.png'

    complex_icon = [["Microsoft Excel", 'xls'], ['Microsoft Office Word', 'doc'],
                    ['Microsoft Office PowerPoint', 'ppt'], ['RAR archive data', 'rar']]
    for i in complex_icon:
        if i[0] in file_type:
            return '/static/image/icons/online/512px/' + i[1] + '.png'

    if 'text' in file_type.lower():
        if '.py' in full_path:
            return '/static/image/icons/online/512px/' + 'py' + '.png'
        if '.cpp' in full_path:
            return '/static/image/icons/online/512px/' + 'cpp' + '.png'
        return '/static/image/icons/online/512px/' + 'txt' + '.png'
    return None


def thumb(request):
    data = retrieve_param(request)

    target_file = unquote(data["target"])
    #cl(target_file)
    full_path = transformDirToInternal(target_file)
    the_file = get_thumb_file(full_path)
    return return_file_data(the_file)


def return_file_data(the_file):
    filename = os.path.basename(unicode(the_file))
    response = HttpResponse(FileWrapper(open(the_file, 'rb')),
                            content_type=mimetypes.guess_type(the_file)[0])
    response['Content-Length'] = os.path.getsize(the_file)
    response['Content-Disposition'] = u"attachment; filename=%s" % urlquote(filename)
    return response


def image(request):
    data = retrieve_param(request)
    the_file = data["path"]
    return return_file_data(the_file)


def gen_qr_code(request):
    #objects = UfsObj.objects.all()
    data = retrieve_param(request)
    return render_to_response('qrcode.html', {"qrcode_file_path": get_qr_code(data["data"])},
                              context_instance=RequestContext(request))