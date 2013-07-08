# -*- coding: gbk -*-
import collections
import json
import time

class Msg(collections.MutableMapping):
    '''
    用来规范化一些属性的名字，比如full path经常被不同的属性名fullpath, full_path代表
    '''
    #Path related
    def add_path(self, full_path):
        self.__setitem__("full_path", full_path)
    def get_path(self):
        return self["full_path"]
        
    #Timestamp related
    def add_timestamp(self):
        if self.has_key("timestamp"):
            cl("Regenerate a timestamp, may not be an expected behaviour")
        self.timestamp = time.time()
        self["timestamp"] = self.timestamp
    def get_timestamp(self):
        return self["timestamp"]
        
    def to_json(self):
        return json.dumps(self, sort_keys=True, indent=4)
        
    def is_stop_msg(self):
        if self.has_key("cmd"):
            if self["cmd"] == "stop":
                cl("Stop msg received")
                return True
        return False
        
        

        
class RegMsg(Msg):
    def add_receiver(self, receiver):
        self["cmd_msg_q"] = receiver.get_cmd_msg_q_name()
    def add_app_name(self, appname):
        self["app_name"] = appname
    # def is_register_ok(self):
        # return False
        
    def to_json(self):
        self.pid = os.getpid()
        print "current pid: ", self.pid
        if self.has_key("app_name") and self.has_key("cmd_msg_q"):
            #Added other required fields for registration msg
            self["cmd"] = "registration"
            return super(RegMsg, self).to_json()
        else:
            raise "Invalid reg msg"
