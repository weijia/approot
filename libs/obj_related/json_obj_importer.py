# -*- coding: utf-8 -*-
import json
from objsys.view_utils import get_ufs_obj_from_json
from objsys.models import UfsObj, ObjRelation


def import_objects_from_json_full_path(updated_item_full_path):
    '''
    {"server":"allbookmarks.duapp.com", "downloaded":[
    {"meta": {"limit": 20, "next": "/objsys/api/ufsobj/ufsobj/?offset=20&limit=20&format=json",
    "offset": 0, "previous": null, "total_count": 184}, "objects": [{"description": "",
    "full_path": "", "head_md5": "", "id": 2, "resource_uri": "/objsys/api/ufsobj/ufsobj/2/",
    "size": null, "tags": ["all_history"], "timestamp": "2013-08-18T04:54:59", "total_md5": "",
    "ufs_url": "http://blog.csdn.net/id19870510/article/details/8489486", "uuid":
    "09006587-787a-4814-8133-1a716d8b5968", "valid": true}]}
    ]}
   '''
    fp = open(updated_item_full_path, "r")
    info = json.load(fp)
    fp.close()
    server = info["server"]
    for downloaded_item in info["downloaded"]:
        for item in ["objects"]:
            referencer_url = server + item["resource_uri"]
            referencer_obj, created = UfsObj.get_or_create(referencer_url, valid=True)
            referenced_obj = get_ufs_obj_from_json(item)
            referenced_obj.tags = ','.join(item["tags"])
            ObjRelation.get_or_create(from_obj=referencer_obj, to_obj=referenced_obj,
                                      relation="Referencing", valid=True)





