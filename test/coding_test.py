import os
from subprocess import Popen


root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
exclude_files = 'venv,build,dest,dist,tmp,__init__.py,.*,conf.py'


def test_coding():
    cmd = ['flake8', root, '--exclude', exclude_files]
    assert Popen(cmd).wait() == 0
