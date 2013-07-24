'''
Created on 2012-02-13

@author: Richard
'''
import libsys
from libs.services.svc_base.msg_service import MsgQ
#from libs.services.svc_base.managed_service import WorkerBase
from libs.services.svc_base.simple_service_v2 import SimpleService, SimpleServiceWorker

gMsgLoggingServiceName = 'tube_logging_service_tube'


class LoggingThreadThread(SimpleServiceWorker):
    def __init__(self, param_dict):
        param_dict.update({"input": "system_tagging_service_input_msg_q"})

    def processItem(self, msg):
        q = MsgQ(self.get_output_msg_queue_name())
        q.send(msg)

        return True


if __name__ == "__main__":
    s = SimpleService({
                          "input": "input tube name",
                          "output": "output tube name, optional",
                          #"blacklist": "blacklist for scanning, example: *.exe",
                      },
                      worker_thread_class=LoggingThreadThread,
                      service_default_input_msg_queue_name=gMsgLoggingServiceName)
    s.run()