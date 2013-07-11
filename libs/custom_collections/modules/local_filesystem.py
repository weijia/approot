import os
import urllib2


def get_collection(path):
    res = []
    #print 'in get_collection'
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        if os.path.isdir(full_path):
            res.append({"data": filename, "attr": {"url": "/filemanager/listdir/path=" + full_path,
                                                 "id": urllib2.quote("local_filesystem://"+full_path)},
                        "state": "closed"
            })
    return res
