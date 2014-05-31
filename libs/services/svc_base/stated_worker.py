import threading
from ufs_diagram.django_processor_state import DjangoProcessorState


class StatedWorker(threading.Thread):
    def __init__(self, processor_uuid, parent, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(StatedWorker, self).__init__(group, target, name, args, kwargs, verbose)
        self.processor_uuid = processor_uuid
        self.state = DjangoProcessorState(processor_uuid)
        self.parent = parent

    def is_quitting(self):
        return self.parent.is_quitting()
