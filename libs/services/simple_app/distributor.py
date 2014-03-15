# -*- coding: gbk -*-
import logging
import thread
from services.pyro_service.pyro_simple_app_base import PyroSimpleAppBase
from services.simple_app.tag_enum_lib.certain_tag_enum_worker import CertainTaggedItemEnumWorker

log = logging.getLogger(__name__)


class Distributor(PyroSimpleAppBase):
    #########################
    # Called through pyro only
    #########################
    def put_msg(self, msg):
        log.debug(msg)
        #noinspection PyBroadException
        try:
            self.handle_req(msg)
        except Exception:
            import traceback

            traceback.print_exc()

    def handle_req(self, msg):
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    s = Distributor()
    s.start_daemon_register_and_launch_loop()
