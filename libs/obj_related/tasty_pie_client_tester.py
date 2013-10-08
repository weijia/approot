import unittest
import libsys
from libs.obj_related.period_manager import NoPersistentOffsetPeriodManager, get_tasty_client_period_manager
from libs.obj_related.tasty_pie_client import download_from_tasty_pie_server, ServerInfo
from test_keys import hostname, username, password


class TastyPieClientTestCase(unittest.TestCase):
    def test_download_from_tasty_pie_server(self):
        server_info = ServerInfo(hostname, username, password)
        periods = get_tasty_client_period_manager("test_state")
        res = download_from_tasty_pie_server(server_info, periods)
        print res


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TastyPieClientTestCase('test_download_from_tasty_pie_server'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
