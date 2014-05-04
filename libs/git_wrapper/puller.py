import logging
import os
from subprocess import PIPE
import traceback
import git
import sys

log = logging.getLogger(__name__)


class RemoteRepo(object):
    def __init__(self, remote_repo):
        self.remote_repo = remote_repo

    @staticmethod
    def get_ref_name(ref):
        return ref.name.split('/')[-1]

    def pull_branch(self, branch):
        for remote_ref in self.remote_repo.refs:
            log.warning("remote ref:", remote_ref)  #origin/master
            self.pull_and_push_changes(branch, remote_ref, self.remote_repo)

    def pull(self, remote_branch_name):
        print 'pulling changes:', remote_branch_name
        #Added istream to avoid error: WindowsError: [Error 6] The handle is invalid
        try:
            self.remote_repo.pull(remote_branch_name, istream=PIPE)
        except AssertionError:
            print 'assert error may be caused by inconsistent log format between git and gitpython'

    def push(self, branch, remote_ref):
        print 'pushing changes'
        self.remote_repo.push(remote_ref.__str__().split('/')[-1],
                              istream=PIPE)

    def pull_and_push_changes(self, branch, remote_ref):
        #print remote_ref#gitbucket/20130313_diagram_rewrite
        if branch.name in self.get_ref_name(remote_ref):
            print 'remote commit: ', remote_ref.commit, remote_ref.commit.message
            self.pull(self.get_ref_name(remote_ref))
            if branch.commit != remote_ref.commit:
                print 'different to remote'
                print 'latest remote log:', remote_ref.commit.message
                self.push(branch, remote_ref)
                print 'latest local log:', branch.commit.message


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
        try:
            len(remote_repo.refs)
        except AssertionError, e:
            e.print_exc()
            print remote_repo
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
                    log.warning("remote branch:", remote_ref)
                    #self.pull_and_push_changes(branch, remote_branch, remote_repo)
                    RemoteRepo(remote_repo).pull_and_push_changes(branch, remote_ref)
                    
try:
    from repo import proj_list, git_path
except:
    repo = []
    git_path = 'C:\\Program Files (x86)\\Git\\bin'


def add_git_to_path():
    os.environ['PATH'] += ";"+git_path
    #print os.environ['PATH']

add_git_to_path()
def main():

    for path in proj_list:
        print "processing:", path
        p = Puller(path)
        p.pull_all()


if __name__ == '__main__':
    add_git_to_path()
    main()