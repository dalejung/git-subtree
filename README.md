git-subtree
===========

Python module to help manage git subtreees. 

I require `pandas` because I am a horrible person and am using it only for display output...

Example `subtrees` file localted at repo root.

```
ctools docroot/sites/all/modules/contrib/ctools git@drupaldale.github.com:drupaldale/ctools.git 7.x-1.x
panels docroot/sites/all/modules/contrib/panels git@drupaldale.github.com:drupaldale/panels.git 7.x-3.x
```

## Install

```
pip install git-subtree
```

## Commands

```
st status
st list
st add_remote
st checkout
st pull
st push
```

## TODO

Remove `pandas` requirement
