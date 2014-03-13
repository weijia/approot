from django.conf import settings
from services.svc_base.diagram_manager_base import DiagramManagerBase


class PyroDiagramManager(DiagramManagerBase):
    def stop_diagram(self):
        super(PyroDiagramManager, self).stop_diagram()

    def start_diagram(self):
        super(PyroDiagramManager, self).start_diagram()