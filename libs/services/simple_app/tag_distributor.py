import logging
from ufs_django_conf import *
from services.pyro_service.pyro_simple_app_base import PyroSimpleAppBase

log = logging.getLogger(__name__)


class TagDistributor(PyroSimpleAppBase):
    #########################
    # Called through pyro only
    #########################
    def put_msg(self, msg):
        log.debug(msg)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    s = TagDistributor()
    s.start_service()
