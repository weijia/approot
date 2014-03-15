import json
import logging
from iconizer.pyro_service_base import PyroServiceBase
from services.pyro_service.simple_app_base import SimpleAppBase
log = logging.getLogger(__name__)


class PyroSimpleAppBase(PyroServiceBase, SimpleAppBase):
    #########################
    # Called through pyro only
    #########################
    def put_msg(self, msg):
        """
        {
            "diagram":{"diagram_id": "xxx-xxxxx-xxxxx",
                "processor_id": "xxx-xxxxx-xxxxx",
            },
            "is_all_tag": False,
            "tag": "git_repo"
        }
        """
        log.error(json.dumps(msg, indent=4))
        #noinspection PyBroadException
        try:
            self.handle_req(msg)
        except Exception:
            import traceback
            traceback.print_exc()

    def start_service(self):
        if not self.is_checking_properties():
            self.start_daemon_register_and_launch_loop()