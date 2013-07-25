import json
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "rootapp.settings"

from django.conf import settings
from ui_framework.objsys.models import UfsObj
from ui_framework.connection.models import Processor


class StatefulProcessor(object):
    def get_processor_ufs_obj(self, processor_id):
        processor_obj_list = UfsObj.objects.filter(uuid=processor_id)
        if 0 == processor_obj_list.count():
            processor_obj = UfsObj(uuid=processor_id)
            processor_obj.save()
        else:
            processor_obj = processor_obj_list[0]
        return processor_obj

    def get_state(self, processor_id, default_param_dict):
        processor_obj = self.get_processor_ufs_obj(processor_id)

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

    def set_state(self, processor_id, param_dict):
        processor_obj = self.get_processor_ufs_obj(processor_id)

        param_str = json.dumps(param_dict)

        processor_list = Processor.objects.filter(ufsobj=processor_obj)
        if 0 == processor_list.count():
            processor = Processor(ufsobj=processor_obj, param_descriptor=param_str, diagram_obj=processor_obj)
            processor.save()
        else:
            processor = processor_list[0]
            processor.param_descriptor = param_str
            processor.save()

