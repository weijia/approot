import argparse
import os
from libs.logsys.logSys import cl
from libs.services.svc_base.msg import Msg
from libs.utils.filetools import get_main_file
import libsys
import sys
from managed_service import ManagedService
from msg_based_service_mgr import MsgBasedServiceManager, gMsgBasedServiceManagerMsgQName


'''
class SimpleWorkThread(beanstalkWorkingThread):
    def __init__(self, input_tube, output_tube):
        super(SimpleWorkThread, self).__init__(input_tube)
        self.output_tube = output_tube
        self.thread_init()
        
    def thread_init(self):

        #A function sub-class can override to do some initialization.
        pass
        
    def add_task_info(self, item):
        self.task_info_item = item
        self.diagram_id = item["diagram_id"]
        self.session_id = item["session_id"]
        
    def output(self, item):
        self.put_item(item, self.output_tube)
'''


class DefaultServiceClass(ManagedService):
    """
    Default main service class
    Service default data input msg queue name: worker thread class name + "_default_input_msg_q_name"
    """
    def __init__(self, param_dict, worker_thread_class):
        """
        Constructor
        """
        # Must set worker_thread_class before calling __init__. As it will be used in get_input_msg_queue_name
        self.worker_thread_class = worker_thread_class
        cl(self.worker_thread_class.__name__)
        super(DefaultServiceClass, self).__init__(param_dict)
        self.task_signature_to_worker_thread = {}

    def add_worker_thread(self, task_signature, thread_instance):
        self.task_signature_to_worker_thread[task_signature] = thread_instance

    def get_input_msg_queue_name(self):
        cl("service input msg queue name", self.worker_thread_class.__name__ + "_default_input_msg_q_name")
        return self.worker_thread_class.__name__ + "_default_input_msg_q_name"

    def is_processing(self, task_signature):
        return self.task_signature_to_worker_thread.has_key(task_signature)

    def process(self, msg):
        """
        Create worker thread if needed.
        :param msg:
        :return:
        """
        t = self.worker_thread_class(msg)
        task_signature = t.get_task_signature()
        if self.is_processing(task_signature):
            print 'input tube already processing: ', task_signature
            return True  # Return True if we do not need to exit msg_loop
            #TODO: add some checking for worker thread, so if no input and output, the work thread can
        #refuse to work
        t.add_task_info(msg)
        self.add_worker_thread(task_signature, t)
        t.start()
        return True  # Return True if we do not need to exit msg_loop

    def on_stop(self):
        """
        Set all sub processor to stop
        :return:
        """
        for task in self.task_signature_to_worker_thread:
            task.stop()


class SimpleService(object):
    def __init__(self, param_dict, service_class=None, worker_thread_class=None):
        #print "inside service.__init__()"
        #param_dict() # Prove that function definition has completed
        #print param_dict
        self.param_dict = param_dict
        self.service_class = service_class
        self.worker_thread_class = worker_thread_class

    def add_task_and_run_service(self, service_instance, args):
        #Generate params
        param = {}
        for i in self.param_dict:
            if args[i] is None:
                continue
            param[i] = args[i]
        for i in ['session_id', 'diagram_id']:
            param[i] = args[i]
        '''
        #Confirm service for this app is started
        service_manager = MsgBasedServiceManager(
            {"input": gMsgBasedServiceManagerMsgQName, "session_id": param["session_id"]})
        #print "exe filename:", __main__.__file__
        #import __main__
        app_name = get_main_file()
        msg = Msg()
        msg.add_app_name(app_name)
        msg.add_session_id(param["session_id"])
        msg.add_cmd("start")
        service_manager.add_msg(msg)
        '''
        #print 'start app'
        service_instance.add_msg(param)
        service_instance.start_service()

    def parse_service_args(self):
        parser = argparse.ArgumentParser()
        #print self.param_dict
        ############################
        # Default parameters
        parser.add_argument("--startserver", help="if the app is called to start the server", action="store_true")
        #"session_id": "Used to identify this session, so previous session msg will be ignored",
        #now default in simple processor
        parser.add_argument("--session_id", help="the session id for all processors in one diagram is unique," +
                                                 "so processors can identify legacy data in tubes using this")
        #"diagram_id": "Each process diagram has an ID, it is used to save diagram related parameters",
        #now default in simple processor
        parser.add_argument("--diagram_id", help="the diagram id used to retreive diagram state " +
                                                 "(get from the diagram processor's param)")
        #######################
        # add all custom parameters
        for i in self.param_dict:
            parser.add_argument("--" + i, help=self.param_dict[i])

        #parser.add_argument("other", help="other options", nargs='*')
        print sys.argv
        #print parser
        args = vars(parser.parse_args())
        return args

    def run(self):
        #print "inside service.__call__()"
        args = self.parse_service_args()

        #print '-----------------everything OK'
        is_server = args["startserver"]

        if self.service_class is None:
            if self.worker_thread_class is None:
                raise "Neither a service class nor a thread class is given, we will not work with nothing"
            service_instance = DefaultServiceClass(args, self.worker_thread_class)
        else:
            service_instance = self.service_class(args)

        #print is_server
        print '----------------------', args
        if service_instance.is_server_only() or is_server:
            print 'start server'
            service_instance.start_service()
        else:
            self.add_task_and_run_service(service_instance, args)


if __name__ == "__main__":
    s = SimpleService({
        "output": "Output msg queue for this generator",
    })
    #s.run()