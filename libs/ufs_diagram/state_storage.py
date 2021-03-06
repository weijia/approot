class MethodNotImplemented(Exception):
    pass


class NoParamDefined(Exception):
    pass


#noinspection PyMethodMayBeStatic
class StateStorageBase(object):
    def get_state(self):
        raise MethodNotImplemented

    def save_state(self, state_dict):
        raise MethodNotImplemented

    def get_state_dict(self, default_dict):
        try:
            self.get_raw_state(default_dict)
        except:
            return default_dict

    def get_state_value(self, state_key, default_value):
        state_dict = self.get_state_dict({state_key: default_value})
        return state_dict.get(state_key, default_value)