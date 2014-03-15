import threading
from services.svc_base.diagram_state import DiagramState


class StatedWorker(threading.Thread):
    def __init__(self, diagram_id, parent, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(StatedWorker, self).__init__(group, target, name, args, kwargs, verbose)
        self.diagram_id = diagram_id
        self.state = DiagramState(diagram_id)
        self.parent = parent

    def is_quitting(self):
        return self.parent.is_quitting()
