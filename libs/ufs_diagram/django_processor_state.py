import json
import logging
from connection.models import Processor
from ufs_diagram.state_storage import StateStorageBase, NoParamDefined

log = logging.getLogger(__name__)


class DjangoProcessorState(StateStorageBase):
    def __init__(self, processor_uuid):
        self.processor_uuid = processor_uuid

    def get_raw_state(self):
        #log.error(self.processor_uuid)
        processor = Processor.objects.get(uuid=self.processor_uuid)
        if (not (processor.param_descriptor is None)) and (not (processor.param_descriptor == "")):
            log.error("loaded from db:"+processor.param_descriptor)
            return json.loads(processor.param_descriptor)
        raise NoParamDefined

    def get_state(self):
        try:
            return self.get_raw_state()
        except NoParamDefined:
            return {}

    def save_state(self, state_dict):
        processor, created = Processor.objects.get_or_create(uuid=self.processor_uuid)
        processor.param_descriptor = json.dumps(state_dict)
        processor.save()