import argparse
import sys


class SimpleAppBase(object):
    DEFAULT_PARAM = {"input": "default processor param",
                     "output": "default processor param",
                     "session_id": "the session id for all processors in one diagram is unique," +
                                   "so processors can identify legacy data in tubes using this",
                     "diagram_id": "the diagram id used to retrieve diagram state " +
                                   "(get from the diagram processor's param)",
    }

    def __init__(self):
        super(SimpleAppBase, self).__init__()
        self.parser = None
        self.init_cmd_line()

    def add_param_from_dict(self, param_dict):
        for i in param_dict:
            self.parser.add_argument("--" + i, help=param_dict[i])

    def parse_service_args(self):
        self.parser = argparse.ArgumentParser()
        #print self.param_dict

        #######################
        # add all custom parameters
        self.add_param_from_dict(self.DEFAULT_PARAM)
        #parser.add_argument("other", help="other options", nargs='*')
        print sys.argv
        #print parser
        args = vars(self.parser.parse_args())
        return args

    def init_cmd_line(self):
        #print "inside service.__call__()"
        args = self.parse_service_args()