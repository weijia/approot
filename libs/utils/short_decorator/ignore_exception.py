import traceback


def ignore_exc(func):
    def wrap_with_exc():
        #noinspection PyBroadException
        try:
            func()
        except:
            traceback.print_exc()
            pass
    return wrap_with_exc