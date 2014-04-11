import os
from obj_related.json_obj import import_objects_from_json_full_path
from ufs_utils.obj_tools import get_hostname
from folder_update_checker import FolderUpdateChecker
from folder_update_checker.file_timestamp_keeper import FileCollectionExistenceInfoKeeper


def import_objects_from_full_path(file_full_path):
    root, ext = os.path.splitext(file_full_path)
    if ext == '.7z':
        plain_text_file_full_path = extract_7z_file(file_full_path)
    plain_text_file_full_path = file_full_path
    import_objects_from_json_full_path(plain_text_file_full_path)


def import_from_tasty_pie_dump_root(g_dump_root_folder, collection_id_for_saved_state):
    """
    Two alternatives to import data, 两种方式：
    1. import data immediately after download, 在下载时立即导入数据库
    2. import data when changes are detected in folders, 在下载时不导入数据库，后面通过检查目录更新导入数据库。
    """
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
                import_objects_from_full_path(updated_item_full_path)


class FolderContaining7z(object):
    def __init__(self, root_for_extracted, folder_containing_7z_root):
        """
        working_foler must exist, we'll not check the existence here
        """
        self.root_for_extracted = root_for_extracted
        self.folder_containing_7z_root = folder_containing_7z_root
        from compress.dec_7z import FolderStructureSync
        self.structure_sync = FolderStructureSync(self.folder_containing_7z_root, self.root_for_extracted)

    def extract(self, full_path_for_7z):
        folder, filename = os.path.split(full_path_for_7z)
        #target_filename = filename.replace(".7z", ".json")
        target_folder = self.structure_sync.get_target_folder(folder)
        #os.path.join(target_folder, filename)