import logging
from iconizer.pyro_service_base import PyroServiceBase
import libsys
from git_wrapper.puller import Puller


class PullService(PyroServiceBase):
    def pull(self, path):
        puller = Puller(path)
        puller.pull_all()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    pull_service = PullService()
    pull_service.start_daemon_register_and_launch_loop()