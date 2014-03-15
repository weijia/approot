from iconizer.pyro_service_base import PyroServiceBase
from services.pyro_service.simple_app_base import SimpleAppBase
from services.svc_base.stoppable import Stoppable


class PyroSimpleAppBase(PyroServiceBase, SimpleAppBase):
    pass