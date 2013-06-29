import argparse

def dummy():
    pass

#Ref: http://blog.csdn.net/beckel/article/details/3585352
class service(object):
    def __init__(self, param_dict):
        #print "inside service.__init__()"
        #param_dict() # Prove that function definition has completed
        #print param_dict
        self.param_dict = param_dict
 
    def __call__(self, service_func):
        #print "inside service.__call__()"
        parser = argparse.ArgumentParser()
        #print self.param_dict
        parser.add_argument("--startserver", help="if the app is called to start the server", action="store_true")
        for i in self.param_dict:
            parser.add_argument("--"+i, help=self.param_dict[i])
        #parser.add_argument("other", help="other options", nargs='*')
        
        #print parser
        args = parser.parse_args()
        
        #print '-----------------everything OK'
        
        is_server = args.startserver
        #print is_server
        if is_server:
            print 'start server'
            service_func(is_server)
        else:
            #Added task
            print 'start app'
            service_func(is_server, args)
        return dummy
        



    
