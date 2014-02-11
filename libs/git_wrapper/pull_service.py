import libsys
from git_wrapper.puller import Puller
from services.pyro_service.pyro_service_base import PyRoServiceBase


class PullService(PyRoServiceBase):
    def pull(self, path):
        puller = Puller(path)
        puller.pull_all()


if __name__ == '__main__':
    pull_service = PullService()
    pull_service.register()