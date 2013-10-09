from libs.obj_related.json_obj import JsonDecoderForUfsObj
from libs.utils import transform as transform
from libs.utils.obj_tools import getUfsUrlForPath

__author__ = 'Richard'


def get_ufs_obj_from_ufs_url(ufs_url):
    obj_list = UfsObj.objects.filter(ufs_url=ufs_url)
    if 0 == obj_list.count():
        obj = UfsObj(ufs_url=ufs_url)
        obj.save()
    else:
        obj = obj_list[0]
    return obj


def get_ufs_obj_from_json(json_dict):
    decoded_obj = JsonDecoderForUfsObj(json_dict)
    if decoded_obj.is_full_path_valid() and decoded_obj.is_ufs_url_valid():
        ufs_obj, created = get_or_create_ufs_obj_from_path_and_url(decoded_obj.get_full_path(),
                                                                   decoded_obj.get_ufs_url())
    elif (not decoded_obj.is_ufs_url_valid()) and (not decoded_obj.is_full_path_valid()):
        print "Invalid json dict:", json_dict
        raise "Invalid json dict"
    else:
        ufs_obj, created = UfsObj.objects.get_or_create(**decoded_obj.get_ufs_obj_attribute_dict(), valid=True)
    return ufs_obj


def get_or_create_ufs_obj_from_path_and_url(full_path, ufs_url):
    """
    full_path and ufs_url must not be empty (""), will be checked here
    """
    if ("" == full_path) or ("" == ufs_url):
        print "Invalid parameter:", full_path, ufs_url
        raise "Invalid parameter"
    if 0 == UfsObj.objects.filter(full_path=full_path, valid=True).count():
        return UfsObj.objects.get_or_create(ufs_url=ufs_url, valid=True)

    for ufs_obj in UfsObj.objects.filter(full_path, valid=True):
        if ufs_obj.ufs_url == ufs_url:
            return ufs_obj, False
        else:
            print "UFS Url not match while full path is equal", full_path, ufs_url, ufs_obj.ufs_url
            raise "UFS Url not match while full path is equal"


def get_ufs_obj_from_full_path(full_path):
    full_path = transform.format_folder_path(full_path)
    obj_list = UfsObj.objects.filter(full_path=full_path)
    if 0 == obj_list.count():
        ufs_url = getUfsUrlForPath(full_path)
        obj = UfsObj(ufs_url=ufs_url, full_path=full_path)
        obj.save()
    else:
        obj = obj_list[0]
    return obj