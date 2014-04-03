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