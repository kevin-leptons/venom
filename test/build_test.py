from sys import executable
from subprocess import Popen


def test_build_and_dist():
    assert Popen([executable, 'ctl', 'clean']).wait() == 0
    assert Popen([executable, 'ctl', 'build']).wait() == 0
    assert Popen([executable, 'ctl', 'dist']).wait() == 0
