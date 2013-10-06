import json
#import urllib2
import httplib2
from libs.obj_related.period_manager import NoPersistentOffsetPeriodManager


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
    @staticmethod
    def get_dumped_data(server_info, period):
        url = "http://%s/objsys/api/ufsobj/ufsobj/?offset=%d&limit=%d&format=json&" \
              "username=%s&password=%s" % (server_info.get_hostname(), period.get_start(), period.get_size(),
                                            server_info.get_username(), server_info.get_password())

        h = httplib2.Http()
        resp, content = h.request(url, "GET")
        downloaded_item = json.loads(content)
        print downloaded_item
        if 0 == len(downloaded_item["objects"]):
            raise NoMoreItems
        return downloaded_item


def download_from_tasty_pie_server(server_info, period_enumerator):
    res = {"server": server_info.get_hostname()}
    NoPersistentOffsetPeriodManager()
    downloaded = []
    for period in period_enumerator.enum_period():
        try:
            downloaded.append(TastyPieClient.get_dumped_data(server_info, period))
        except NoMoreItems:
            break
    res["downloaded"] = downloaded
    return res