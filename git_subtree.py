import git
import subprocess

FILE = "/Users/datacaliber/Dropbox/projects/doubleprime/domains/afab/subtrees"

def find_toplevel():
  toplevel = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'])
  toplevel = toplevel.strip()
  return toplevel

class SubTree(object):
  def __init__(self, prefix, remote, branch):
    self.prefix = prefix
    self.remote = remote
    self.remote_alias = remote_alias
    self.branch = branch

  def __repr__(self):
    return "SubTree({prefix}, {remote}, {remote_alias}, {branch})".format(**self.__dict__)

if __name__ == '__main__':

  with open(FILE) as f:
    lines = [line.split() for line in f.read().split('\n') if line]
    subtrees = [SubTree(prefix, remote, branch) for prefix, remote, remote_alias, branch in lines]

  toplevel = find_toplevel()

  repo = git.Repo(toplevel)

  print toplevel
  print subtrees
