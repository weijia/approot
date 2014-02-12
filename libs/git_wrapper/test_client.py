import Pyro4
from repo import proj_list

if __name__ == '__main__':
    uri_string = "PYRONAME:PullService"
    git_puller = Pyro4.Proxy(uri_string)
    #git_puller.pull('D:\\userdata\\q19420\\workspace\\SharingPark-Server\\')
    for proj in proj_list:
        git_puller.pull(proj)
