import os


class CollectionInterface(object):
    def __contains__(self, item):
        pass


class StorageWithTransactionInterface(object):
    def start_transaction(self):
        pass

    def commit_transaction(self):
        pass


class FolderUpdateChecker(object):
    def __init__(self,  root_folder, collection):
        """
        Folder structure:
            2013
                01
                    12345678.901
                    12345678.902
                    ...
                02
        """
        self.root_folder = root_folder
        self.collection = collection

    def enum_new_file(self):
        """
        This is the simplest approach for update checking, maybe refine this to avoid scan all files every time by
        using modified time for folders.
        """
        for dirpath, dirnames, filenames in os.walk(self.root_folder):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                self.collection.is_updated()

    '''
    def get_updated_sub_folders(self, folder_full_path):
        for sub_folder in os.listdir(folder_full_path):
            sub_folder_full_path = os.path.join(folder_full_path, sub_folder)

            if self.collection.is_updated(sub_folder_full_path):
                pass

    def enum_updated_files(self):
        scan_list = os.listdir(self.root_folder)
        #Check the first level
        for folder in scan_list:
            year_folder_list = os.listdir(self.root_folder)
        for year_folder in year_folder_list:
            year_folder_full_path = os.path.join(self.root_folder, year_folder)
            if os.path.isdir(year_folder_full_path):

                 month_folder_list = os.listdir(year_folder_full_path)
                 for month_folder_name in month_folder_list:
                     month_folder_full_path = os.path.join(year_folder_full_path, month_folder_name)
                     if os.path.isdir(month_folder_full_path):
                         filenames = os.listdir(month_folder_full_path)
                         filenames.sort(reverse=True)
                         for filename in filenames:
                             yield os.path.join(month_folder_full_path, filename)
    '''
