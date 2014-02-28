import Pyro4
from msg_service_interface import MsgServiceInterface, UnknownReceiver


class PyroMsgService(MsgServiceInterface):
    """
    Receiver is a string indicate the receiver's name, it may contain protocol string to specify message sending
     protocol
    """
    def send_to(self, receiver, msg):
        #Locate NS
        ns = Pyro4.locateNS()
        #Find service name as receiver
        service_dict = ns.list()
        #Send to receiver by calling handle function of the service
        if receiver in service_dict:
            proxy = Pyro4.Proxy(service_dict[receiver])
            proxy._pyroOneway.add("put_msg")
            proxy.put_msg(msg)
        else:
            print "unknown receiver:", receiver
            raise UnknownReceiver

