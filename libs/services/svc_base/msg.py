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

    def __str__(self):
        return self.store.__str__()

    def add_path(self, full_path):
        self.store["full_path"] = full_path

    def get_path(self):
        return self["full_path"]

    #Timestamp related
    def add_timestamp(self):
        if "timestamp" in self.store:
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

    def is_cmd(self):
        if "cmd" in self.store:
            return True
        return False

    def is_stop_msg(self):
        if self.is_cmd():
            if self["cmd"] == "stop":
                cl("Stop msg received")
                return True
        return False

    def get_session_id(self):
        return self.get("session_id", 0)

    def add_app_name(self, app_name):
        self["app_name"] = app_name
        return self

    def has_app_name(self):
        return self.APP_NAME_ATTR_NAME in self.store

    def get_app_name(self):
        return self[self.APP_NAME_ATTR_NAME]

    def add_session_id(self, session_id):
        self["session_id"] = session_id

    def get_cmd_q_name(self):
        return self[self.CMD_MSG_Q_NAME_ATTR]

    def is_pid_match(self):
        return os.getpid() == self["pid"]


class RegMsg(Msg):
    def add_receiver(self, receiver):
        self["cmd_msg_q"] = receiver.get_cmd_msg_q_name()
        return self

    def is_registration_ok(self):
        return self["registration_result"]

    def set_registration_result(self, is_ok):
        self["registration_result"] = is_ok

    def to_json(self):
        pid = os.getpid()
        print "current pid: ", pid
        if (self.APP_NAME_ATTR_NAME in self.store) and (self.CMD_MSG_Q_NAME_ATTR in self.store):
            #Added other required fields for registration msg
            self["cmd"] = "registration"
            self["pid"] = pid
            return super(RegMsg, self).to_json()
        else:
            raise "Invalid reg msg"

    def is_valid(self):
        if self.APP_NAME_ATTR_NAME in self.store:
            return True
        else:
            return False