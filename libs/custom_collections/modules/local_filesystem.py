import os
import urllib2
import libsys
import ufs_utils.string_tools as string_tools
from objsys.models import UfsObj
from ufs_utils.obj_tools import get_formatted_full_path


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
        obj_list = UfsObj.objects.filter(full_path=full_path)
        tags = ""
        if 0 != obj_list.count():
            tag_list = []
            for tag in obj_list[0].tags:
                tag_list.append(tag.name)
            if 0 != len(tag_list):
                tags += " tags:(%s)" % (','.join(tag_list))
        if os.path.isdir(full_path):
            id_for_js = string_tools.jsIdEncoding(u"local_filesystem://" + full_path)
            item = {"data": filename + tags,
                        "attr": {
                            "url": u"/object_filter/?query_base=" + string_tools.quote_unicode(
                                u"/filemanager/filesystem_rest/?full_path=" +
                                unicode(full_path)),
                            "id": string_tools.quote_unicode(id_for_js)
                        }
            }
            try:
                for filename in os.listdir(full_path):
                    if os.path.isdir(os.path.join(full_path, filename)):
                        item["state"] = "closed"
                        break
            except:
                pass
            res.append(item)
    return res
