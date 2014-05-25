import json
from connection.models import Processor
from objsys.models import UfsObj
from services.svc_base.svc_interfaces.task_state_interface import TaskStateInterface


class DjangoBasedTaskState(TaskStateInterface):
    def __init__(self):
        super(DjangoBasedTaskState, self).__init__()
        self.inner_log_str = ""
        self.diagram_ufs_url = None
        self.process_ufs_url = None

    def set_state_id(self, process_ufs_url, diagram_ufs_url):
        self.process_ufs_url = process_ufs_url
        self.diagram_ufs_url = diagram_ufs_url

    def load(self):
        return self.load_task_state()

    def save(self, state_dict):
        self.save_task_state(state_dict)

    def save_task_state(self, state):
        task_obj = UfsObj.objects.get(ufs_url=self.process_ufs_url)
        processor = Processor.objects.get(ufsobj=task_obj)
        self.inner_log_str += "processor:" + str(processor) + "\n"
        processor.param_descriptor = json.dumps(state)
        processor.save()
        self.inner_log_str += "saved:" + str(processor.param_descriptor) + "\n"

    def load_task_state(self):
        task_obj, created = UfsObj.objects.get_or_create(ufs_url=self.process_ufs_url)
        diagram_obj, created = UfsObj.objects.get_or_create(ufs_url=self.diagram_ufs_url)
        processor, created = Processor.objects.get_or_create(ufsobj=task_obj, diagram_obj=diagram_obj)
        result = {}
        if (not (processor.param_descriptor is None)) and (not (processor.param_descriptor == "")):
            result = json.loads(processor.param_descriptor)
        self.inner_log_str += str(result)
        return result