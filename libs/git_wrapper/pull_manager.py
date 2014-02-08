import Pyro4

import sys
sys.path.append("D:\\work\\mine\\codes\\ufs_django\\approot")
from libs.git_wrapper.puller import Puller
class PullManager(object):
    def pull(self, path):
        puller = Puller(path)
        puller.pull_all()


if __name__ == '__main__':
    daemon = Pyro4.Daemon()
    puller = daemon.register(PullManager())
    ns = Pyro4.locateNS()
    ns.register("ufs_git_puller", puller)
    daemon.requestLoop()