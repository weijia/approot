import json

from libsys import *

from objsys.models import UfsObj
from connection.models import Processor


class StateManager(object):
    @staticmethod
    def get_processor_ufs_obj(processor_id):
        processor_obj_list = UfsObj.objects.filter(uuid=processor_id)
        if 0 == processor_obj_list.count():
            processor_obj = UfsObj(uuid=processor_id)
            processor_obj.save()
        else:
            processor_obj = processor_obj_list[0]
        return processor_obj

    @staticmethod
    def get_state(processor_id, default_param_dict):
        processor_obj = StateManager.get_processor_ufs_obj(processor_id)

        processor_list = Processor.objects.filter(ufsobj=processor_obj)
        if 0 == processor_list.count():
            param = default_param_dict
            print "default param:", param
            param_str = json.dumps(param)
            processor = Processor(ufsobj=processor_obj, param_descriptor=param_str, diagram_obj=processor_obj)
            processor.save()
        else:
            processor = processor_list[0]
            param_str = processor.param_descriptor
            print "existing param:", param_str
            param = json.loads(param_str)
        return param

    @staticmethod
    def set_state(processor_id, param_dict):
        processor_obj = StateManager.get_processor_ufs_obj(processor_id)

        param_str = json.dumps(param_dict)

        processor_list = Processor.objects.filter(ufsobj=processor_obj)
        if 0 == processor_list.count():
            processor = Processor(ufsobj=processor_obj, param_descriptor=param_str, diagram_obj=processor_obj)
            processor.save()
        else:
            processor = processor_list[0]
            processor.param_descriptor = param_str
            processor.save()