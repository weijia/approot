import json
from jsonrpc import jsonrpc_method
from objsys.tastypie_related.tastypie_import import TastypieImporter
import jsonrpc.proxy

@jsonrpc_method('json_rpc_services.import_objects_from_local_file')
def import_objects_from_local_file(request, file_full_path):
    fp = open(file_full_path, "r")
    file_dict = json.load(fp)
    fp.close()
    importer = TastypieImporter()
    importer.import_data_from_tastypie_result(file_dict)


@jsonrpc_method('json_rpc_services.hello')
def whats_the_time(request, name='Lester'):
    return "Hello %s" % name
