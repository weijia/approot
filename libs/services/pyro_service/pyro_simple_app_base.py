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

    def handle_req(self, msg):
        """
        The msg will also include processor parameters, so do not need to retrieve params from processor again here
        """
        pass

    def start_service(self):
        if not self.is_checking_properties():
            log.debug("is not checking properties")
            #print "is not checking properties"
            self.start_daemon_register_and_launch_loop()
        log.debug("quitting start service")