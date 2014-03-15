# -*- coding: gbk -*-
import logging
import libtool
libtool.include_sub_folder_in_root_path(__file__, "approot", "libs")
from services.pyro_service.pyro_simple_app_base import PyroSimpleAppBase

log = logging.getLogger(__name__)


class Distributor(PyroSimpleAppBase):
    def handle_req(self, msg):
        pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    s = Distributor()
    if not s.is_checking_properties():
        s.start_daemon_register_and_launch_loop()
