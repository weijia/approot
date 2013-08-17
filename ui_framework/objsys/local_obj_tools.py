from libs.utils import transform as transform
from libs.utils.obj_tools import getUfsUrlForPath
from ui_framework.objsys.models import UfsObj


def get_ufs_obj_from_ufs_url(ufs_url):
    obj_list = UfsObj.objects.filter(ufs_url=ufs_url)
    if 0 == obj_list.count():
        obj = UfsObj(ufs_url=ufs_url)
        obj.save()
    else:
        obj = obj_list[0]
    return obj


def get_ufs_obj_from_full_path(full_path):
    full_path = transform.transformDirToInternal(full_path)
    obj_list = UfsObj.objects.filter(full_path=full_path)
    if 0 == obj_list.count():
        ufs_url = getUfsUrlForPath(full_path)
        obj = UfsObj(ufs_url=ufs_url, full_path=full_path)
        obj.save()
    else:
        obj = obj_list[0]
    return obj