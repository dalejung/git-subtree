from distutils.core import setup

DISTNAME='git_subtree'
FULLVERSION='0.2'

setup(
    name=DISTNAME,
    version=FULLVERSION,
    scripts=['bin/st'],
    packages=[
        'git_subtree'
    ],
    install_requires=[
        'tabulate',
        'gitpython>=1.0'
    ],
)
