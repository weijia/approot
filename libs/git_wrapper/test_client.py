import Pyro4
import sys
sys.path.append("D:\\work\\mine\\codes\\ufs_django\\approot")

if __name__ == '__main__':
    uri_string = "PYRONAME:ufs_git_puller"
    git_puller = Pyro4.Proxy(uri_string)
    git_puller.pull('D:\\userdata\\q19420\\workspace\\SharingPark-Server\\')
