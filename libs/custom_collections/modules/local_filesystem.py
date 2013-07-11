import os
import urllib2
import libsys
import libs.utils.string_tools as string_tools
from ui_framework.objsys.models import UfsObj
from libs.utils.objTools import get_formatted_full_path

def get_collection(path):
    """
    Used to generate the tree structure
    :param path:
    :return:
    """
    res = []
    #print 'in get_collection'
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        full_path = get_formatted_full_path(full_path)
        obj_list = UfsObj.objects.filter(full_path = full_path)
        tags = ""
        if 0 != obj_list.count():
            tags += "("
            for tag in obj_list[0].tags:
                tags += tag.name
            tags += ")"
        if os.path.isdir(full_path):
            res.append({"data": filename + tags,
                        "attr": {
                            "url": string_tools.quote_unicode(u"/filemanager/filesystem_rest/?full_path=" +
                                                              unicode(full_path)),
                            "id": string_tools.quote_unicode(u"local_filesystem://" + full_path)
                        },
                        "state": "closed"
            })
    return res
