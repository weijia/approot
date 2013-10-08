import json
import unittest
from libs.app_framework.folders import get_or_create_app_data_folder
from libs.utils.filetools import get_free_timestamp_filename_in_path
import libsys
from libs.obj_related.period_manager import NoPersistentOffsetPeriodManager, get_tasty_client_period_manager
from libs.obj_related.tasty_pie_client import download_from_tasty_pie_server, ServerInfo
from test_keys import hostname, username, password


class TastyPieClientTestCase(unittest.TestCase):
    def test_download_from_tasty_pie_server(self):
        server_info = ServerInfo(hostname, username, password)
        period_manager = get_tasty_client_period_manager("test_state")
        res = download_from_tasty_pie_server(server_info, period_manager)
        export_folder = get_or_create_app_data_folder("tastypie_exported")
        output_filename = get_free_timestamp_filename_in_path(export_folder, ".txt")
        print res
        fp = open(output_filename, 'w')
        json.dump(res, fp, indent=4)
        fp.close()
        period_manager.save()


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TastyPieClientTestCase('test_download_from_tasty_pie_server'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
