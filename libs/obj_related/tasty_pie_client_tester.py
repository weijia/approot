
import unittest
from obj_related.tasty_pie_client import ServerInfo, TastyPieClient
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
