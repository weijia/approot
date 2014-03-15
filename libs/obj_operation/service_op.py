from iconizer.pyro_launcher import get_app_name_from_full_path
from utils.django_utils import retrieve_param, get_json_resp
from services.sap.service_manager_sap import ServiceManager


def start(request):
    data = retrieve_param(request)
    app_name = get_app_name_from_full_path(data["ufs_url"])
    ServiceManager().start_service(app_name)
    res = {"log": "done"}
    return get_json_resp(res)
