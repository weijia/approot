# -*- coding: gbk -*-
import collections
import json
import os
import time
import libsys
from libs.logsys.logSys import *


class Msg(collections.MutableMapping):
    """
    用来规范化一些属性的名字，比如full path经常被不同的属性名fullpath, full_path代表
    """
    #Path related
    APP_NAME_ATTR_NAME = "app_name"
    CMD_MSG_Q_NAME_ATTR = "cmd_msg_q"
    CMD_ATTR_NAME = "cmd"
    
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs)) # use the free update to set keys

    def __getitem__(self, key):
        #return self.store[self.__keytransform__(key)]
        return self.store[key]

    def __setitem__(self, key, value):
        #self.store[self.__keytransform__(key)] = value
        self.store[key] = value

    def __delitem__(self, key):
        #del self.store[self.__keytransform__(key)]
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    #def __keytransform__(self, key):
    #    return key
        
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
        return self

    def get_timestamp(self):
        return self["timestamp"]
        
    def to_json(self):
        return json.dumps(self.store, sort_keys=True, indent=4)

    def add_cmd(self, cmd):
        self["cmd"] = cmd
        return self
        
    def is_stop_msg(self):
        if "cmd" in self:
            if self["cmd"] == "stop":
                cl("Stop msg received")
                return True
        return False

    def get_session_id(self):
        return self["session_id"]

    def has_app_name(self):
        return self.has_key(self.APP_NAME_ATTR_NAME)
        
        

        
class RegMsg(Msg):
    def __init__(self, *args):
        super(RegMsg, self).__init__(args)

    def add_receiver(self, receiver):
        self["cmd_msg_q"] = receiver.get_cmd_msg_q_name()
        return self

    def add_app_name(self, app_name):
        self["app_name"] = app_name
        return self

    def is_registration_ok(self):
        return self["registration_result"]

    def set_registration_result(self, is_ok):
        self["registration_result"] = is_ok
        
    def to_json(self):
        self.pid = os.getpid()
        print "current pid: ", self.pid
        if self.has_key(self.APP_NAME_ATTR_NAME) and self.has_key(self.CMD_MSG_Q_NAME_ATTR):
            #Added other required fields for registration msg
            self["cmd"] = "registration"
            return super(RegMsg, self).to_json()
        else:
            raise "Invalid reg msg"

    def is_valid(self):
        if self.has_key(self.APP_NAME_ATTR_NAME):
            return True
        else:
            return False

    def get_app_name(self):
        return self[self.APP_NAME_ATTR_NAME]

    def get_cmd_q_name(self):
        return self[self.CMD_MSG_Q_NAME_ATTR]