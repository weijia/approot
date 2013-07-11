import os
import urllib2
import libsys
import libs.utils.string_tools as string_tools


def get_collection(path):
    res = []
    #print 'in get_collection'
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        if os.path.isdir(full_path):
            res.append({"data": filename,
                        "attr": {
                                    "url": string_tools.quote_unicode(u"/filemanager/filesystem_rest/?full_path="+
                                                                      unicode(full_path)),
                                    "id": string_tools.quote_unicode(u"local_filesystem://"+full_path)
                                },
                        "state": "closed"
            })
    return res
