import subprocess

def find_toplevel(dir=None):
    """
    Given a dir within a repo, find the top level directory
    """
    toplevel = subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], cwd=dir)
    toplevel = toplevel.strip().decode('utf-8')
    return toplevel
