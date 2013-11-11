import subprocess

import git
from util import find_toplevel

def require_clean(func):
    """
    @decorator
    subtree commands require that the repo have no working changes
    """
    fname = func.__name__
    def _func(self):
        if self.repo.is_dirty():
            raise Exception("{fname} needs a clean repo without outstanding \
                            working changes".format(fname=fname))
        return func(self)
    _func.__name__ = fname
    return _func

class SubTree(object):
    def __init__(self, name, prefix, remote_url, branch, remote_alias=None,
                 repo=None):
        self.name = name
        self.prefix = prefix
        self.remote_url = remote_url
        if remote_alias is None:
            remote_alias = name
        self.remote_alias = remote_alias
        self.branch = branch

        if repo is None:
            repo = self.default_repo()
        self.repo = repo

    def __repr__(self):
        attrs = ['name', 'prefix', 'remote_url', 'branch']
        if self.name != self.remote_alias:
            attrs.append('remote_alias')
        attr_format = ", ".join(["{k}={{{k}}}".format(k=k) for k in attrs])
        out_format = "SubTree({0})".format(attr_format)
        return out_format.format(**self.__dict__)

    def default_repo(self):
        toplevel = find_toplevel()
        repo = git.Repo(toplevel)
        return repo

    @property
    def remote(self):
        remote = getattr(self.repo.remotes, self.remote_alias, None)
        return remote

    def check_remote(self):
        remote = self.remote
        if remote is None:
            return False
        return remote.url == self.remote_url

    def add_remote(self):
        remote = self.remote
        if remote and remote.url != self.remote_url:
            raise Exception("Remote {remote_alias} exists but has wrong url. \
                    \nCorrect: {remote_url}\nCurrent: {current_url}".format(
                        remote_alias=self.remote_alias, remote_url=self.remote_url
                        , current_url=remote.url))

        if remote:
            return "Remote Already Exists"

        self.repo.create_remote(self.remote_alias, self.remote_url)
        remote = self.remote
        assert remote.url == self.remote_url
        return "Remote Added"

    @property
    def toplevel(self):
        return self.repo.working_dir

    def subtree_command(self, cmd):
        cmds = []
        cmds.append(cmd)
        output = subprocess.check_output("; ".join(cmds), shell=True, cwd=self.toplevel)
        return output

    def fetch(self):
        self.remote.fetch()

    @property
    def tree(self):
        tree = self.repo.active_branch.commit.tree
        try:
            subtree = tree[self.prefix]
        except KeyError:
            subtree = None

        return subtree

    def has_tree(self):
        return self.tree is not None

    @require_clean
    def checkout(self):
        if not self.check_remote():
            self.add_remote()

        if self.has_tree():
            return "{0} already checked out".format(self.prefix)

        self.fetch()
        cmd = "git subtree add --prefix={prefix} {remote_alias}/{branch} --squash".format(**self.__dict__)
        return self.subtree_command(cmd)

    @require_clean
    def pull(self):
        if not self.has_tree():
            raise Exception("Must Checkout First")

        cmd = "git subtree pull --prefix={prefix} {remote_alias} {branch} --squash".format(**self.__dict__)
        return self.subtree_command(cmd)

    @require_clean
    def push(self):
        if not self.has_tree():
            raise Exception("Must Checkout First")

        cmd = "git subtree push --prefix={prefix} {remote_alias} {branch} --squash".format(**self.__dict__)
        return self.subtree_command(cmd)
