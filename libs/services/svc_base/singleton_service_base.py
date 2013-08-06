import libsys
from libs.services.svc_base.managed_service import ManagedService


class SingletonServiceBase(ManagedService):
    def process(self):
        pass

    def on_stop(self):
        pass

