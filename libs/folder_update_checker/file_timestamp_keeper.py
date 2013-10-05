from libs.utils.obj_tools import get_ufs_obj_from_full_path
from ui_framework.collection_management.models import CollectionItem
from ui_framework.objsys.models import UfsObj


class FileTimestampKeeperInterface(object):
    def __init__(self, root_folder):
        pass

    def is_updated(self, full_path):
        pass


class FileCollectionExistenceKeeper(FileTimestampKeeperInterface):
    def __init__(self, root_folder, keeper_uuid):
        self.keeper_uuid = keeper_uuid

    def is_updated(self, full_path):
        ufs_obj, created = UfsObj.objects.get_or_create(full_path=full_path, valid=True)
        if 0 == CollectionItem.objects.filter(obj=ufs_obj, uuid=self.keeper_uuid).count():
            return True
        return False

    def update(self, full_path):
        ufs_obj, created = UfsObj.objects.get_or_create(full_path=full_path, valid=True)
        CollectionItem.objects.get_or_create(obj=ufs_obj, uuid=self.keeper_uuid)
