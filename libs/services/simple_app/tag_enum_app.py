# -*- coding: gbk -*-
import logging
import thread
from services.pyro_service.pyro_simple_app_base import PyroSimpleAppBase
from services.simple_app.tag_enum_lib.certain_tag_enum_worker import CertainTaggedItemEnumWorker

log = logging.getLogger(__name__)


class TagEnumApp(PyroSimpleAppBase):
    def __init__(self):
        super(TagEnumApp, self).__init__()
        #Only one service request should be processed for one diagram (as tag enumerator is a generator)
        self.diagram_to_task = {}

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
        log.debug(msg)
        #noinspection PyBroadException
        try:
            self.handle_req(msg)
        except Exception:
            import traceback

            traceback.print_exc()

    def handle_req(self, msg):
        diagram_id = msg["diagram"]["diagram_id"]
        processor_id = msg["diagram"]["processor_id"]
        if diagram_id in self.diagram_to_task:
            raise "Duplicated request"
        task = CertainTaggedItemEnumWorker(processor_id, self)
        self.diagram_to_task[diagram_id] = task
        task.start()


def test():
    import time

    time.sleep(15)
    from services.sap.msg_service_sap import AutoRouteMsgService

    AutoRouteMsgService().send_to("tag_enum_app", {
        "diagram": {
            "diagram_id": "xxx-xxxxx-xxxxx",
            "processor_id": "xxx-xxxxx-xxxxx",
        },
        "is_all_tag": False,
        "tag": "git_repo"
    })


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    s = TagEnumApp()
    thread.start_new_thread(test, ())
    s.start_daemon_register_and_launch_loop()
