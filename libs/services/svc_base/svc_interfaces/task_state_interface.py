class TaskStateInterface(object):
    #noinspection PyMethodMayBeStatic
    def load(self):
        return {}

    def save(self, state_dict):
        pass
