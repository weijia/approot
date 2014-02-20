import libsys
from git_wrapper.puller import Puller
from services.pyro_service.pyro_service_base import PyRoServiceBase


class DispatchService(PyRoServiceBase):
    @staticmethod
    def dispatch(msg_dict):
        #Find diagram
        diagram_descriptor = {"diagram": "",
                              "msg": {}}
        #Find next processor's msg queue name

        #Send msg to the receiver's msg queue
        pass


if __name__ == '__main__':
    dispatch_service = DispatchService()
    dispatch_service.register()