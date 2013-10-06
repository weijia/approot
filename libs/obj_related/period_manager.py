
class Period(object):
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
    def enum_period(self):
        pass


class NoPersistentOffsetPeriodManager(PeriodManagerInterface):
    def __init__(self, size=40):
        self.offset = 0
        self.size = size

    def enum_period(self):
        yield Period(self.offset, self.offset + self.size - 1)
        self.offset += self.size
