import logging
from simple_app_import_lib import *
from config.conf_storage import ConfStorage
from services.pyro_service.pyro_simple_app_base import PyroSimpleAppBase
from ufs_utils.web.direct_opener import open_url


log = logging.getLogger(__name__)


class UrlOpener(PyroSimpleAppBase):
    def handle_req(self, msg):
        target_url = msg["target_url"]
        target_url = target_url.replace("$UFS_SERVER_AND_PORT", ConfStorage.get_ufs_server_and_port_str())
        log.error("opening: %s" % target_url)
        open_url(target_url)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    url_opener = UrlOpener()
    #pull_service.init_cmd_line()
    url_opener.start_service()