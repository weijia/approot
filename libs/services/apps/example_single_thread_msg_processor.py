"""
This example is based on tagging service
"""
import libsys
from libs.logsys.logSys import cl
from libs.services.svc_base.simple_service_v2 import SimpleService
from libs.services.svc_base.managed_service import ManagedService


class ExampleSingleThreadServiceMsgProcessor(ManagedService):
    def __init__(self, param_dict):
        param_dict.update({"input": "example_single_thread_service_msg_q_name"})
        super(ExampleSingleThreadServiceMsgProcessor, self).__init__(param_dict)

    def process(self, msg):
        #Return True if we don't want to quit msg_loop
        return True

    def is_server_only(self):
        """
        In simple_service_v2, if this function return true, this service will be treated only as server, so no task
        will be added
        :return: True if it is single thread service.
        """
        return True

    def on_stop(self):
        return True   # Return true to accept stop

if __name__ == "__main__":
    s = SimpleService({}, ExampleSingleThreadServiceMsgProcessor)
    s.run()