import logging
from iconizer.pyro_service_base import PyroServiceBase

log = logging.getLogger(__name__)


class TagDistributor(PyroServiceBase):
    #########################
    # Called through pyro only
    #########################
    def put_msg(self, msg):
        log.debug(msg)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    s = TagDistributor()
    s.start_daemon_register_and_launch_loop()
