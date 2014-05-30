import logging
#There are 2 ufs_django_conf file in the codes. In exe, the file in root will be used. Otherwise, simple app
# use the local file located in service/simple_apps
from ufs_django_conf import *
from services.pyro_service.pyro_simple_app_base import PyroSimpleAppBase
from git_wrapper.puller import Puller


class PullService(PyroSimpleAppBase):

    def handle_req(self, msg):
        self.pull(msg["full_path"])

    def pull(self, path):
        puller = Puller(path)
        puller.pull_all()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    pull_service = PullService()
    #pull_service.init_cmd_line()
    pull_service.start_service()