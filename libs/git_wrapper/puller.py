from subprocess import PIPE
import traceback
import git


class RemoteRepo(object):
    def __init__(self, remote_repo):
        self.remote_repo = remote_repo

    @staticmethod
    def get_ref_name(ref):
        return ref.name.split('/')[-1]

    def pull_branch(self, branch):
        for remote_ref in self.remote_repo.refs:
            print "remote ref:", remote_ref  #origin/master
            self.pull_and_push_changes(branch, remote_ref, self.remote_repo)

    def pull(self, remote_branch_name):
        print 'pulling changes'
        #Added istream to avoid error: WindowsError: [Error 6] The handle is invalid
        self.remote_repo.pull(remote_branch_name, istream=PIPE)

    def push(self, branch, remote_ref):
        print 'pushing changes'
        self.remote_repo.push(remote_ref.__str__().split('/')[-1],
                              istream=PIPE)

    def pull_and_push_changes(self, branch, remote_ref):
        #print remote_ref#gitbucket/20130313_diagram_rewrite
        if branch.name in self.get_ref_name(remote_ref):
            print 'remote commit: ', remote_ref.commit
            print 'latest remote log:', remote_ref.commit.message
            if branch.commit != remote_ref.commit:
                print 'different to remote'
                self.pull(self.get_ref_name(remote_ref))
                self.push(branch, remote_ref)
                print 'latest local log:', branch.log()[-1].message


class Puller(object):
    def __init__(self, full_path):
        self.full_path = full_path

    def pull_all(self):
        r = git.Repo(self.full_path)
        local_active_branch = r.active_branch
        print 'current branch:', local_active_branch.name, local_active_branch.commit

        for remote_repo in r.remotes:
            print "remote repo", remote_repo
            self.process_remote_repo(local_active_branch, remote_repo)

    @staticmethod
    def is_repo_ref_valid(remote_repo):
        #if hasattr(i, "refs"):
        #    print 'no refs attr'
        #print "length:", len(i.refs)
        is_ref_valid = True
        if True:#try:
            len(remote_repo.refs)
        else:#except:
            is_ref_valid = False
        return is_ref_valid

    @staticmethod
    def is_ignored(url):
        #if "https" in url:
        #    print 'ignoring :', url
        #    return True
        #else:
        #    return False
        return False

    def process_remote_repo(self, branch, remote_repo):
        if not self.is_ignored(remote_repo.url):
            if self.is_repo_ref_valid(remote_repo):
                for remote_ref in remote_repo.refs:
                    print "remote branch:", remote_ref
                    #self.pull_and_push_changes(branch, remote_branch, remote_repo)
                    RemoteRepo(remote_repo).pull_and_push_changes(branch, remote_ref)


def main():
    #p = Puller('D:\\userdata\\q19420\\workspace\\SharingPark-Server')
    #p = Puller('D:\\work\mine\\SharingPark-Android\\SharingPark-Android')
    #p = Puller('D:\\work\\mine\\codes\\sharepark_interact')
    p = Puller('D:\\work\\mine\\codes\\ufs_django\\approot')
    p.pull_all()


if __name__ == '__main__':
    main()