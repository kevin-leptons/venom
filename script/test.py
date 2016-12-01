import os
from subprocess import Popen

root_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
test_dir = os.path.join(root_path, 'test')


def run_test():
    return Popen(['pytest', test_dir]).wait()
