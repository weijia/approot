import json
import os
from libs.folder_update_checker import FolderUpdateChecker
from libs.folder_update_checker.file_timestamp_keeper import FileCollectionExistenceInfoKeeper
from libs.utils.obj_tools import get_hostname
from ui_framework.objsys.models import UfsObj, ObjRelation
from ui_framework.objsys.view_utils import get_ufs_obj_from_json


class JsonDecoderForUfsObj(object):
    """
    TODO: may automatically generate every attribute getter for this class.
    """
    def __init__(self, json_dict):
        self.json_dict = json_dict

    def get_full_path(self):
        return self.json_dict["full_path"]

    def get_ufs_url(self):
        return self.json_dict["ufs_url"]

    def is_full_path_valid(self):
        if ("full_path" in self.json_dict) and ("" != self.json_dict["full_path"]):
            return True
        return False

    def is_ufs_url_valid(self):
        if ("ufs_url" in self.json_dict) and ("" != self.json_dict["ufs_url"]):
            return True
        return False

    def get_valid_attribute_dict(self):
        res = {}
        for key in self.json_dict:
            if "" != self.json_dict[key]:
                res[key] = self.json_dict[key]
        return res

    def get_ufs_obj_attribute_dict(self):
        valid_attr = self.get_valid_attribute_dict()
        res = {}
        valid_ufs_obj_attribute_name_list = ["full_path", "ufs_url", "size", "total_md5", "head_md5",
                                             "uuid", "description", "description_json"]
        for key in valid_attr:
            if key in valid_ufs_obj_attribute_name_list:
                res[key] = self.json_dict[key]
        return res


def import_objs_from_full_path(updated_item_full_path):
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


def import_from_tastypie_dump_root(g_dump_root_folder, collection_id_for_saved_state):
    file_timestamp_keeper = FileCollectionExistenceInfoKeeper(collection_id_for_saved_state)
    #Get hostname
    self_host_name = get_hostname()
    #Scan other host's data directories.
    for hostname_as_folder in os.listdir(g_dump_root_folder):
        if hostname_as_folder == self_host_name:
            continue
        host_name_as_folder_full_path = os.path.join(g_dump_root_folder, hostname_as_folder)

        if os.path.isdir(host_name_as_folder_full_path):
            checker = FolderUpdateChecker(host_name_as_folder_full_path, file_timestamp_keeper)
            for updated_item_full_path in checker.enum_new_file():
                import_objs_from_full_path(updated_item_full_path)