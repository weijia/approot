import threading


class StoppableThread(threading.Thread):
    def __init__(self):
        super(StoppableThread, self).__init__()
        self.is_quitting_flag = False

    def set_stop(self, is_stop=True):
        self.is_quitting_flag = is_stop

    def is_quitting(self):
        return self.is_quitting_flag