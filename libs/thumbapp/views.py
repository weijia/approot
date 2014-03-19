import os
from urllib import unquote
from django.shortcuts import render_to_response
from django.template import RequestContext

from thumb.thumbInterface import get_thumb
from obj_related.local_obj import LocalObj
from utils.mobile.qrcode_image import get_qr_code
from utils.django_utils import retrieve_param, return_file_data
import libsys
from utils.transform import format_path
from models import ThumbCache
from utils.misc import ensure_dir as ensure_dir
from logsys.logSys import *
from objsys.view_utils import get_ufs_obj_from_full_path


def get_thumb_file(target_file):
    full_path = format_path(target_file)
    if not os.path.exists(full_path):
        the_file = os.path.join(libsys.get_root_dir(), 'static/image/icons/file-broken-icon.png')
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
            the_file = os.path.join(libsys.get_root_dir(), get_icon(full_path, obj.get_type()))
            #raise "No thumb"
    return the_file


def get_icon(full_path, file_type=None):
    if os.path.isdir(full_path):
        return 'static/image/icons/folder-images-icon.png'

    if file_type is None:
        file_type = LocalObj(full_path).get_type()

    cl(full_path, 'file type is:', file_type)

    if 'Zip archive data' in file_type:
        ext = full_path.split('.')[-1]
        for new_office_ext in ["xlsx", "docx", "pptx"]:
            if new_office_ext in ext:
                return 'static/image/icons/online/512px/' + new_office_ext + '.png'

    ext_icons = ['html', 'xml', 'pdf']
    for i in ext_icons:
        if i in file_type.lower().split(" "):
            return 'static/image/icons/online/512px/' + i + '.png'

    complex_icon = [["Microsoft Excel", 'xls'], ['Microsoft Office Word', 'doc'],
                    ['Microsoft Office PowerPoint', 'ppt'], ['RAR archive data', 'rar']]
    for i in complex_icon:
        if i[0] in file_type:
            #print "file_type:", i[1]
            return 'static/image/icons/online/512px/' + i[1] + '.png'

    if 'text' in file_type.lower():
        if '.py' in full_path:
            return 'static/image/icons/online/512px/' + 'py' + '.png'
        if '.cpp' in full_path:
            return 'static/image/icons/online/512px/' + 'cpp' + '.png'
        return 'static/image/icons/online/512px/' + 'txt' + '.png'
    return None


def thumb(request):
    data = retrieve_param(request)

    target_file = unquote(data["target"])
    #cl(target_file)
    full_path = format_path(target_file)
    the_file = get_thumb_file(full_path)
    return return_file_data(the_file)


def image(request):
    data = retrieve_param(request)
    the_file = data["path"]
    return return_file_data(the_file)


def gen_qr_code(request):
    #objects = UfsObj.objects.all()
    data = retrieve_param(request)
    return render_to_response('qrcode.html', {"qrcode_file_path": get_qr_code(data["data"])},
                              context_instance=RequestContext(request))