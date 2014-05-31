#noinspection PyClassHasNoInit
import json
import logging
from connection.models import Processor


log = logging.getLogger(__name__)


class MethodNotImplemented:
    pass


#noinspection PyMethodMayBeStatic
class StateStorageBase(object):
    def get_state(self):
        raise MethodNotImplemented

    def save_state(self, state_dict):
        raise MethodNotImplemented


class DjangoProcessorState(StateStorageBase):
    def __init__(self, processor_uuid):
        self.processor_uuid = processor_uuid

    def get_state(self):
        #processor, created = Processor.objects.get_or_create(uuid=self.processor_uuid)
        log.error(self.processor_uuid)
        processor = Processor.objects.get(uuid=self.processor_uuid)
        if (not (processor.param_descriptor is None)) and (not (processor.param_descriptor == "")):
            log.error("loaded from db:"+processor.param_descriptor)
            return json.loads(processor.param_descriptor)
        return {}

    def save_state(self, state_dict):
        processor, created = Processor.objects.get_or_create(uuid=self.processor_uuid)
        processor.param_descriptor = json.dumps(state_dict)
        processor.save()