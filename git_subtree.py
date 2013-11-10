import git
import subprocess

FILE = "/Users/datacaliber/Dropbox/projects/doubleprime/domains/afab/subtrees"

def find_toplevel():
  toplevel = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])
  toplevel = toplevel.strip()
  return toplevel

class SubTree(object):
  def __init__(self, name, prefix, remote_url, branch, remote_alias=None):
    self.name = name
    self.prefix = prefix
    self.remote_url = remote_url
    if remote_alias is None:
      remote_alias = name
    self.remote_alias = remote_alias
    self.branch = branch
    self.repo = None

  def __repr__(self):
    attrs = ['name', 'prefix', 'remote_url', 'branch']
    if self.name != self.remote_alias:
      attrs.append('remote_alias')
    attr_format = ", ".join(["{k}={{{k}}}".format(k=k) for k in attrs])
    out_format = "SubTree({0})".format(attr_format)
    return out_format.format(**self.__dict__)

  def check_remote(self):
    remote = getattr(self.repo.remotes, self.remote_alias, None)
    return remote.url == remote_url


if __name__ == '__main__':

  toplevel = find_toplevel()
  repo = git.Repo(toplevel)

  with open(FILE) as f:
    lines = [line.split() for line in f.read().split('\n') if line]
    subtrees = [SubTree(name, prefix, remote_url, branch) for name, prefix, remote_url, branch in lines]
    for tree in subtrees:
      tree.repo = repo


  for tree in subtrees:
    tree.check_remote()

  print toplevel
  print subtrees
