import json
import unittest
from libs.app_framework.folders import get_or_create_app_data_folder
from libs.utils.filetools import get_free_timestamp_filename_in_path
import libsys
from libs.obj_related.period_manager import NoPersistentOffsetPeriodManager, get_tasty_client_period_manager
from libs.obj_related.tasty_pie_client import ServerInfo, TastyPieClient
from test_keys import hostname, username, password


class TastyPieClientTestCase(unittest.TestCase):
    def test_export_and_encrypt_tasty_pie_data(self):
        server_info = ServerInfo(hostname, username, password)
        c = TastyPieClient(server_info)
        c.export_and_encrypt_tasty_pie_data('test_state', password)


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TastyPieClientTestCase('test_export_and_encrypt_tasty_pie_data'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
