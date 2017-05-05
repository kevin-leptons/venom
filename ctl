#!/usr/bin/env python3

'''
SYNOPSIS

    clt list theme
    ctl build [--clean] [theme-name] [theme-name]...
    ctl dist [--clean]
    ctl dfile osrc sdir dest
    ctl --help

DESCRIPTION

    *list theme* show all of theme names to pass to *build [theme-name]*.

    *build* build all of themes.  

    *build --clean* clean all of build files.
    
    *build theme-name...* build specify themes by names, list by
    *list theme*

    *build --clean theme-name...* clean specific build files of themes.

    *dist* pack theme into package in 'dist/venom_<version>_all.deb'.

    *dist --clean* clean all of distribution files.

    *dfile* merge two directories into dest directory.

    *--help* show help information.

AUTHORS

    Kevin Leptons <kevin.leptons@gmail.com>
'''

import os
import sys
import shutil
import click
from os import path
from os.path import isdir, realpath, dirname
from sys import executable

from tool.logger import stdlog, stat_done, stat_err
from tool.builder import Version, PkgSpec, pkg_build_clean, pkg_build, \
                         pkg_dist, pkg_dist_clean, list_theme
from tool.util import real_theme_name, short_theme_name
from tool.test import run_test
from tool.shell import rm


ROOT = realpath(dirname(__file__))

pkg_ver = Version(1, 3, 0)
pkg_spec = PkgSpec('venom', pkg_ver, ROOT, path.join(ROOT, 'src'),
                   path.join(ROOT, 'dest'), path.join(ROOT, 'dist'),
                   path.join(ROOT, 'test'))


@click.group()
def cli():
    pass


@cli.group(help='List attribtues')
def list():
    pass


@list.command(help='List theme names')
def theme():
    list_theme()


@cli.command(help='Build theme packages')
@click.argument('names', nargs=-1)
@click.option('--clean', is_flag=True, help='Clean build files')
def build(names, clean):
    if clean:
        pkg_build_clean(pkg_spec, names)
    else:
        pkg_build(pkg_spec, names)


@cli.command(help='Pack venom into package')
@click.option('--clean', is_flag=True, help='Clean distribution files')
def dist(clean):
    if clean:
        pkg_dist_clean(pkg_spec)
    else:
        pkg_dist(pkg_spec)


@cli.command(help='Merger two directory in dest directory')
@click.argument('odir')
@click.argument('sdir')
@click.argument('dest')
def dfile(odir, sdir, dest):
    diff_file(odir, sdir, dest)


@cli.command(help='Run unit tests')
def test():
    assert run_test() == 0


cli()
