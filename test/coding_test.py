import os
from subprocess import Popen


root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
exclude_files = 'venv,build,dest,dist,tmp,__init__.py,.cache,.*,conf.py'


def test_coding():
    cmd = ['flake8', root, '--exclude', exclude_files]
    res = Popen(cmd).wait()

    assert res == 0
