'''
SPEC    : Run all of unit test

EXPORT  : run_test()

AUTHOR  : kevin leptons <kevin.leptons@gmail.com>
'''

import os
from subprocess import Popen

root_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
test_dir = os.path.join(root_path, 'test')


def run_test():
    '''
    Use pytest to run all of unit tests in 'test' directory
    '''

    return Popen(['pytest', test_dir]).wait()
