#!/usr/bin/env python

#
# Use for python 2.7
#

import platform
import sys
import shutil
from os import path, makedirs
from urllib import urlretrieve
from subprocess import Popen
from setuptools import setup, find_packages, Command

root = path.realpath(path.dirname(__file__))


class InitCommand(Command):
    user_options = []
    description = 'Install essential package to manager python'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # install pip - python package manager
        url = 'https://bootstrap.pypa.io/get-pip.py'
        tmp_dir = path.join(root, 'tmp')
        install_file = path.join(tmp_dir, 'install-pip.py')
        if not path.isdir(tmp_dir):
            makedirs(tmp_dir)
        urlretrieve(url, install_file)
        if Popen([sys.executable, install_file]).wait() != 0:
            sys.exit(1)

        # install virtualenv package
        cmd = ['pip', 'install', 'virtualenv']
        if platform.os.name == 'posix':
            cmd.insert(0, 'sudo')
        if Popen(cmd).wait() != 0:
            sys.exit(1)

        # create virtual environment
        if Popen(['virtualenv', 'venv']).wait() != 0:
            sys.exit(1)


class CleanCommand(Command):
    user_options = []
    description = 'Clean all of build result'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        shutil.rmtree(path.join(root, '.cache'), True)
        shutil.rmtree(path.join(root, 'dist'), True)
        shutil.rmtree(path.join(root, 'build'), True)
        shutil.rmtree(path.join(root, 'dest'), True)
        shutil.rmtree(path.join(root, '*.egg-info'), True)
        shutil.rmtree(path.join(root, '.eggs'), True)
        shutil.rmtree(path.join(root, 'tmp'), True)


class CleanVenvCommand(Command):
    user_options = []
    description = 'Clean virtual environment'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        venv_dir = path.join(root, 'venv')
        shutil.rmtree(venv_dir, True)


class DevCommand(Command):
    user_options = []
    description = 'Install packages for development'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # install develop packages
        dev_file = path.join(root, 'dev-requires.txt')
        if Popen(['pip', 'install', '-r', dev_file]).wait() != 0:
            sys.exit(1)

        # install runtime dependency packages
        if Popen(['pip', 'install', '-e', '.']).wait() != 0:
            sys.exit(1)


setup(
    name='venom',
    version='0.0.1',
    description='control gnome theme',
    long_description='https://github.com/kevin-leptons/venom',
    keywords='gtk gnome theme linux mono-color',
    author='kevin leptons',
    author_email='kevin.leptons@gmail.com',
    url='https://github.com/kevin-leptons/venom',
    download_url='https://github.com/kevin-leptons/venom',
    install_requires=['click'],
    packages=find_packages(exclude=['script', 'test']),
    entry_points={
        'console_scripts': [
            'venom=venom.cli:cli',
        ]
    },
    cmdclass={
        'init': InitCommand,
        'clean': CleanCommand,
        'cleanvenv': CleanVenvCommand,
        'dev': DevCommand,
    }
)
