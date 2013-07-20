import json
import os

import libsys
from libs.services.svc_base.beanstalkd_interface import beanstalkServiceApp
from django.conf import settings
from ui_framework.objsys.models import UfsObj, CollectionItem
from django.utils.timezone import utc
from libs.services.svc_base.simpleservice import SimpleService
from libs.utils.misc import ensureDir as ensure_dir
from django.contrib.auth.models import User
from libs.services.svc_base.state import StatefulProcessor
from ui_framework.connection.save_diagram_view import save_diagram
from libs.services.svc_base.service_starter import diagram_root


gDiagramImporterProcessorId = 'f4156981-575d-4057-b6f7-269307105f80'


class DiagramImporter(beanstalkServiceApp, StatefulProcessor):
    def startServer(self):
        root_dir = libsys.get_root_dir()
        dump_root = os.path.join(root_dir, "../diagrams/")
        ensure_dir(dump_root)

        param = self.get_state(gDiagramImporterProcessorId, {"timestamp": 0})
        if True:
            last_timestamp = param["timestamp"]
            print last_timestamp
            anonymous = User.objects.filter(pk=settings.ANONYMOUS_USER_ID)[0]
            for filename in os.listdir(dump_root):
                cur_timestamp = float(filename.replace('.json', ''))
                if cur_timestamp > last_timestamp:
                    file = open(os.path.join(dump_root, filename), 'r')
                    data = json.load(file)
                    diagram_id = data["diagram_id"]
                    diag_obj_list = UfsObj.objects.filter(ufs_url = u"diagram://" + diagram_id)
                    if 0 == diag_obj_list.count():
                        save_diagram(data, anonymous, False)
                        
                    diag_obj_list = UfsObj.objects.filter(ufs_url = u"diagram://" + diagram_id) 
                    diag_obj = diag_obj_list[0]
                    #Add diagram to initial launched app
                    
                    coll_list = CollectionItem.objects.filter(obj = diag_obj)
                    if 0 == coll_list.count():
                        CollectionItem(obj = diag_obj, id_in_col = diagram_id, user = anonymous, uuid=diagram_root).save()
        
        ######
        # Quitting, so save last_timestamp
        param["timestamp"] = last_timestamp
        self.set_state(gDiagramImporterProcessorId, param)
                
        
    
        
if __name__ == "__main__":
    s = SimpleService({
                            "input": "Input tube for generator",
                            "output": "Output tube for generator",
                      },
                      DiagramImporter)
    s.run()