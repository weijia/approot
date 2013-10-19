import json
import beanstalkc
from configuration import g_config_dict
gBeanstalkdServerHost = '127.0.0.1'
gBeanstalkdServerPort = g_config_dict["ufs_beanstalkd_port"]


class BeanstalkMsgService(object):
        def sendto(self, receiver, msg_dict):
            #print 'port: ', gBeanstalkdServerPort
            beanstalk = beanstalkc.Connection(host=gBeanstalkdServerHost, port=gBeanstalkdServerPort)
            try:
                beanstalk.use(receiver)
            except:
                print 'using: "%s" failed' % receiver
            s = json.dumps(msg_dict, sort_keys=True, indent=4)
            print "add item: %s, to: %s" % (s, receiver)
            job = beanstalk.put(s)
            return job
