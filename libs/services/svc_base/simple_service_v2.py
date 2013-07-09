import argparse
import libsys
import sys
from managed_service import ManagedService
from msg_based_service_mgr import MsgBasedServiceManager


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
    '''
    classdocs
    '''
    def __init__(self, worker_thread_class):
        '''
        Constructor
        '''
        tube_name = "default_service_msg_queue_for_" + worker_thread_class.__name__
        super(DefaultServiceClass, self).__init__(tube_name)
        self.worker_thread_class = worker_thread_class
        self.task_signature_to_worker_thread = {}

    def add_worker_thread(self, task_signature, thread_instance):
        self.task_signature_to_worker_thread[task_signature] = thread_instance
        
    def is_processing(self, task_signature):
        return self.task_signature_to_worker_thread.has_key(task_signature)
    
    def process(self, msg):
        t = self.worker_thread_class(msg)
        task_signature = t.get_task_signiture()
        if self.is_processing(task_signature):
            print 'input tube already processing: ',task_signature
            return True #Return True if we do not need to exit msg_loop
        t.add_task_info(msg)
        self.add_worker_thread(task_signature, t)
        t.start()
        return True #Return True if we do not need to exit msg_loop


class SimpleService(object):
    def __init__(self, param_dict, service_class = None, worker_thread_class = None):
        #print "inside service.__init__()"
        #param_dict() # Prove that function definition has completed
        #print param_dict
        self.param_dict = param_dict
        self.service_class = service_class
        self.worker_thread_class = worker_thread_class


    def add_task(self, service_instance, args):
        #Confirm service for this app is started
        service_manager = MsgBasedServiceManager()
        service_manager.add_item({})
        print 'start app'
        #Generate params
        param = {}
        for i in self.param_dict:
            param[i] = args[i]
        for i in ['session_id', 'diagram_id']:
            param[i] = args[i]
        service_instance.add_item(param)

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
            service_instance = DefaultServiceClass(self.worker_thread_class)
        else:
            service_instance = self.service_class()
            
        #print is_server
        if is_server:
            print 'start server'
            service_instance.start_service()
        else:
            self.add_task(service_instance, args)
        
        
if __name__ == "__main__":
    s = SimpleService({
                            "output": "Output msg queue for this generator",
                      })
    #s.run()