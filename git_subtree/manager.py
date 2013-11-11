"""
Subtree.

Manager Class

"""
import os.path
import subprocess
from collections import OrderedDict

from git_subtree.util import find_toplevel
import git_subtree.subtree as subtree


class MissingTreelist(Exception):

    """"Repo does not have treelist associated with it."""

    pass

def find_treelist(dir=None):
    toplevel = find_toplevel(dir)
    treelist = os.path.join(toplevel, 'subtrees')
    if not os.path.exists(treelist):
        return None
    return treelist

def process_treelist(treelist, repo=None):
    with open(treelist) as f:
        lines = [line.split() for line in f.read().split('\n') if line]
        subtrees = [subtree.SubTree(name, prefix, remote_url, branch, repo=repo)
                    for name, prefix, remote_url, branch in lines]
        return OrderedDict(((s.name, s) for s in subtrees))

def require_treelist(func):
    def _func(self):
        if self.treelist is None:
            raise MissingTreelist()
        return func(self)
    return _func

class SubTreeManager(object):
    def __init__(self, repo, treelist=None):
        self.repo = repo
        self.treelist = treelist

    _subtrees = None
    @property
    def subtrees(self):
        if self._subtrees is None:
            subtrees = process_treelist(self.treelist)
            self._subtrees = subtrees
        return self._subtrees

    @require_treelist
    def list(self):
        return [(k, s) for k, s in self.subtrees.items()]

    @require_treelist
    def checkout(self):
        output = OrderedDict()
        for name, tree in self.subtrees.items():
            output[name] = tree.checkout()
        return output

    @require_treelist
    def pull(self):
        output = OrderedDict()
        for name, tree in self.subtrees.items():
            output[name] = tree.pull()
        return output
