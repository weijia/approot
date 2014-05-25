import json
import logging
from objsys.tastypie_related.tastypie_import import TastypieImporter
from ufs_django_conf import *
from services.pyro_service.pyro_simple_app_base import PyroSimpleAppBase
from jsonrpc.proxy import ServiceProxy


log = logging.getLogger(__name__)


class ObjImportService(PyroSimpleAppBase):
    def handle_req(self, msg):
        full_path = msg["full_path"]
        log.error(full_path)
        for filename in os.listdir(full_path):
            file_full_path = os.path.join(full_path, filename)
            log.error(filename+","+file_full_path)
            s = ServiceProxy('http://localhost:8110/json_rpc_services/json/')
            s.json_rpc_services.import_objects_from_local_file(file_full_path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    obj_importer = ObjImportService()
    #pull_service.init_cmd_line()
    obj_importer.start_service()