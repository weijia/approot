class Stoppable(object):
    def __init__(self):
        super(Stoppable, self).__init__()
        self.is_quitting_flag = False

    def set_stop(self, is_stop=True):
        self.is_quitting_flag = is_stop

    def is_quitting(self):
        return self.is_quitting_flag