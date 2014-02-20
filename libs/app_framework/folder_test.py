import unittest
from folders import get_app_full_path_by_name


class FolderTestCase(unittest.TestCase):
    @staticmethod
    def test_get_app_full_path_by_name():
        print get_app_full_path_by_name("7z")


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(FolderTestCase('test_get_app_full_path_by_name'))

    runner = unittest.TextTestRunner()
    runner.run(suite)