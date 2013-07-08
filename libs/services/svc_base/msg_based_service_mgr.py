# -*- coding: gbk -*-
from service_base import Service


gBeanstalkdLauncherServiceTubeName = "beanstalkd_launcher_service"

class MsgBasedServiceManager(Service):
    def process(self, msg):
        if msg.is_stop_msg():
            #Send stop msg to all registered services
            return False
        
        if msg.has_key("cmd"):
            if msg["cmd"] == "registration":
                #Keep app name, pid, input cmd queue name
                pass
            elif msg["cmd" == "start":
                #Start an app if not started
                pass
            else:
                cl("Unexpected command")
    