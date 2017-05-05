from sys import executable
from subprocess import call


def test_build_and_dist():
    assert call([executable, 'ctl', 'build', '--clean']) == 0
    assert call([executable, 'ctl', 'build', 'black']) == 0

    assert call([executable, 'ctl', 'dist']) == 0
    assert call([executable, 'ctl', 'dist', '--clean']) == 0

    assert call([executable, 'ctl', 'build', '--clean', 'black']) == 0
