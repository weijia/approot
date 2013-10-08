import json
import os
from libs.app_framework.folders import get_or_create_app_data_folder
from libs.utils.misc import ensure_dir
import libsys


class Period(object):
    """
    Include start and end
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_size(self):
        return self.end - self.start + 1


class PeriodManagerInterface(object):
    def enum_spare_period(self):
        pass

    def add_period(self):
        pass


class NoPersistentOffsetPeriodManager(PeriodManagerInterface):
    def __init__(self, size=40):
        self.offset = 0
        self.size = size

    def enum_spare_period(self):
        yield Period(self.offset, self.offset + self.size - 1)
        self.offset += self.size


class SimpleOffsetPeriodManager(PeriodManagerInterface):
    def __init__(self, period_state_file_full_path):
        self.period_state_file_full_path = period_state_file_full_path
        if os.path.exists(period_state_file_full_path):
            fp = open(self.period_state_file_full_path, "r")
            self.state = json.load(fp)
            fp.close()
            self.offset = self.state["offset"]
            self.size = self.state["size"]
        else:
            self.state = {}
            self.offset = 0
            self.size = 40

    def enum_spare_period(self):
        #!!!Keep this value so even self.offset is updated somewhere else, the enumerate will not go wrong!!!
        offset = self.offset
        while offset < 10000:  # prevent unexpected dead loop
            yield Period(self.offset, self.offset + self.size - 1)
            offset += self.size

    def add_period(self, period):
        self.offset = period.get_end()

    def save(self):
        self.state["offset"] = self.offset
        self.state["size"] = self.size
        fp = open(self.period_state_file_full_path, "w")
        json.dump(self.state, fp)
        fp.close()


def get_tasty_client_period_manager(period_manager_id):
    state_path = get_or_create_app_data_folder("period_state")
    state_file_path = os.path.join(state_path, period_manager_id)
    return SimpleOffsetPeriodManager(state_file_path)

