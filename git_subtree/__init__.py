from subtree import SubTree, find_toplevel

FILE = "/Users/datacaliber/Dropbox/projects/doubleprime/domains/afab/subtrees"

if __name__ == '__main__':

  toplevel = find_toplevel()

  with open(FILE) as f:
    lines = [line.split() for line in f.read().split('\n') if line]
    subtrees = [SubTree(name, prefix, remote_url, branch) for name, prefix, remote_url, branch in lines]

  for tree in subtrees:
    tree.add_remote()

  print toplevel
  print subtrees
