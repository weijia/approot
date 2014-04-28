import threading
from git_wrapper.puller import Puller


class SingleClassDiagramService(threading.Thread):
    pass


class SimplePullService(SingleClassDiagramService):
    RUN_EVERY_MIN = 10
    RUN_ON_TAGS = ["git_repo"]

    def handle_req(self, msg):
        self.pull(msg["full_path"])

    def pull(self, path):
        puller = Puller(path)
        puller.pull_all()