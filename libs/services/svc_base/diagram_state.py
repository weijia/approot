from services.svc_base.state import StateManager


class DiagramState(object):
    def __init__(self, diagram_id):
        self.diagram_id = diagram_id
        
    def get_state_dict(self, default_dict):
        return StateManager.get_state(self.diagram_id, default_dict)
        
    def get_state_value(self, state_key, default_value):
        return self.get_state_dict({state_key: default_value})[state_key]
