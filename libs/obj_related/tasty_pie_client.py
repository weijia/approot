import argparse
import httplib
import json
#import urllib2
import os
import urllib
import urllib2
from libs.app_framework.folders import get_or_create_app_data_folder
from libs.compress.enc_7z import EncZipFileOn7Zip
from libs.datetime_storage.datetime_folders import get_date_based_path_and_filename
from libs.utils.filetools import get_free_timestamp_filename_in_path
from libs.utils.obj_tools import get_hostname
import libsys
import httplib2
from libs.obj_related.period_manager import Period, get_tasty_client_period_manager


class NoMoreItems(object): pass


class ServerInfo(object):
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def get_hostname(self):
        return self.hostname

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password


class TastyPieClient(object):
    def __init__(self, server_info):
        self.server_info = server_info

    def get_data_for_empty_periods(self, period_manager):
        downloaded = []
        for period in period_manager.enum_spare_period():
            downloaded_item = self.get_data_for_period(period)
            downloaded.append(downloaded_item)
            downloaded_cnt = len(downloaded_item["objects"])
            if downloaded_cnt != period.get_size():
                new_period = Period(period.get_start(), period.get_start()+downloaded_cnt-1)
                period_manager.add_period(new_period)
                break
            period_manager.add_period(period)

        return downloaded

    def get_data_for_period(self, period):
        url = "http://%s/objsys/api/ufsobj/ufsobj/?offset=%d&limit=%d&format=json&" \
              "username=%s&password=%s" % (self.server_info.get_hostname(), period.get_start(), period.get_size(),
                                           self.server_info.get_username(), self.server_info.get_password())
        #h = httplib2.Http()
        #resp, content = h.request(url, "GET")
        response = urllib2.urlopen(url)
        content = response.read()
        downloaded_items = json.loads(content)
        print downloaded_items
        return downloaded_items

    def download_from_tasty_pie_server(self, period_manager):
        res = {"server": self.server_info.get_hostname()}
        client = TastyPieClient(self.server_info)
        downloaded = client.get_data_for_empty_periods(period_manager)
        res["downloaded"] = downloaded
        return res

    def save_from_tasty_pie_data(self, state_name, output_filename):
        period_manager = get_tasty_client_period_manager(state_name)
        dump_data = self.download_from_tasty_pie_server(period_manager)
        fp = open(output_filename, 'w')
        json.dump(dump_data, fp, indent=4)
        fp.close()
        period_manager.save()

    def export_and_encrypt_tasty_pie_data(self, state_name, password):
        export_folder = get_or_create_app_data_folder("tasty_pie_exported")
        output_filename = get_free_timestamp_filename_in_path(export_folder, ".txt")
        self.save_from_tasty_pie_data(state_name, output_filename)
        folder_for_encrypted_files = get_or_create_app_data_folder("tasty_pie_encrypted")
        local_folder_for_encrypted_files = os.path.join(folder_for_encrypted_files, get_hostname())
        encrypted_file_path = get_date_based_path_and_filename(local_folder_for_encrypted_files)
        storage = EncZipFileOn7Zip(encrypted_file_path, password=password)
        storage.addfile(output_filename)
        storage.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("-m", "--make-argument-true", help="optional boolean argument", action="store_true")
    #parser.add_argument("-o","--make-other-argument-true", help="optional boolean argument 2", action="store_true",  default=True)
    #parser.add_argument("-n","--number", help="an optional number", type=int)
    #parser.add_argument("-r","--restricted-number", help="one of a few possible numbers", type=int, choices=[1,2,3],  default=2)
    #parser.add_argument("-c", "--counting-argument", help="counting #occurrences", action="count")
    #parser.add_argument("-d", "--default-value-argument", help="default value argument", type=float, default="3.14")
    #group = parser.add_mutually_exclusive_group()
    #group.add_argument("-v", "--verbose", action="store_true")
    #group.add_argument("-q", "--quiet", action="store_true")
    #parser.add_argument("posarg", help="positional argument", type=str)
    parser.add_argument("-w", "--webserver", help="Web server hostname", type=str)
    parser.add_argument("-u", "--username", help="Username", type=str)
    parser.add_argument("-p", "--password", help="Password", type=str)
    parser.add_argument("-s", "--state-id", help="Download state ID", type=str)

    args = vars(parser.parse_args())
    s = ServerInfo(args["webserver"], args["username"], args["password"])
    periods = get_tasty_client_period_manager(args["state-id"])
    res = download_from_tasty_pie_server(s, periods)
    print res