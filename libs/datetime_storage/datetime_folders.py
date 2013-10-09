import os
import datetime
import time
from libs.utils import transform as transform, filetools
from libs.utils.filetools import get_free_timestamp_filename_in_path
from libs.utils.misc import ensure_dir


class PathIsNotDirException(Exception): pass


class DateTimeFolder(object):
    def __init__(self, root_folder):
        if not os.path.isdir(root_folder):
            raise PathIsNotDirException
        self.root_folder = root_folder

    def enumerate_from_latest(self):
         year_folder_list = os.listdir(self.root_folder)
         year_folder_list.sort(reverse=True)
         for year_folder in year_folder_list:
             year_folder_full_path = os.path.join(self.root_folder, year_folder)
             if os.path.isdir(year_folder_full_path):
                 month_folder_list = os.listdir(year_folder_full_path)
                 month_folder_list.sort(reverse=True)
                 for month_folder_name in month_folder_list:
                     month_folder_full_path = os.path.join(year_folder_full_path, month_folder_name)
                     if os.path.isdir(month_folder_full_path):
                         filenames = os.listdir(month_folder_full_path)
                         filenames.sort(reverse=True)
                         for filename in filenames:
                             yield os.path.join(month_folder_full_path, filename)

    def get_folder_name_for_today(self):
        now = datetime.datetime.utcnow()
        return os.path.join(self.root_folder, "%s/%s/%s" % (now.year, now.month, time.time()))


if __name__ == "__main__":
    d = DateTimeFolder("d:/")
    cnt = 0
    for i in d.enumerate_from_latest():
        print i
        cnt += 1
        if cnt > 6:
            break

    print d.get_folder_name_for_today()


def get_date_based_path_and_filename(root_folder, ext=".7z"):
    time_value = time.gmtime()
    year_str = time.strftime("%Y", time_value)
    month_str = time.strftime("%m", time_value)
    day_str = time.strftime("%d", time_value)
    date_dir = year_str + "/" + month_str + "/" + day_str
    date_dir_full_path = unicode(os.path.join(root_folder, date_dir))
    ensure_dir(date_dir_full_path)
    file_full_path = transform.transformDirToInternal(
        get_free_timestamp_filename_in_path(date_dir_full_path, ext))
    return file_full_path