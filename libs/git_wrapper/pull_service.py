import sys
sys.path.append("D:\\work\\mine\\codes\\ufs_django\\approot")
from libs.git_wrapper.puller import Puller
from libs.services.pyro_service.pyro_service_base import PyRoServiceBase


class PullService(PyRoServiceBase):
    def pull(self, path):
        puller = Puller(path)
        puller.pull_all()


if __name__ == '__main__':
    puller = PullService()
    puller.register()