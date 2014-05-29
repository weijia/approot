import logging
from simple_app_import_lib import *
from services.pyro_service.pyro_simple_app_base import PyroSimpleAppBase
from ufs_utils.web.direct_opener import open_url


class UrlOpener(PyroSimpleAppBase):
    def handle_req(self, msg):
        open_url(msg["target_url"])


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    url_opener = UrlOpener()
    #pull_service.init_cmd_line()
    url_opener.start_service()