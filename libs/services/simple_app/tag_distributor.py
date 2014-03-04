import logging
from services.pyro_service.pyro_service_base import PyRoServiceBase

log = logging.getLogger(__name__)


class TagDistributor(PyRoServiceBase):
    #########################
    # Called through pyro only
    #########################
    def put_msg(self, msg):
        log.debug(msg)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    s = TagDistributor()
    s.register()
