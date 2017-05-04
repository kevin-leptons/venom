#!/usr/bin/env python3

# DESCRIPTIONS
#
# Build GTK3 theme. Builder will mix color and build theme package.
# It contains
#   - GTK3 theme
#   - GNOME shell theme
#   - Icon theme
#
# USAGE
#
# $ builder build
#
# EXAMPLES
#
# $ builder build venom-green

import os
import sys
import shutil
import click
from os import path
from os.path import isdir, realpath, dirname
from sys import executable

from tool.logger import stdlog, stat_done, stat_err
from tool.builder import Version, PkgSpec, pkg_build, pkg_dist
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


@cli.command(help='List themes')
@click.argument('name', required=False)
def list(name):
    themes = setting.themes

    if name is None:
        # list name of themes

        for name in themes:
            print(short_theme_name(name))
    else:
        # list properties of theme

        name = real_theme_name(name)
        if name not in themes:
            stdlog(stat_err, 'not found theme', name)
            sys.exit(1)

        theme = themes[name]
        print('name: {}'.format(short_theme_name(name)))
        print('front_color: {}'.format(theme.front_color))
        print('back_color: {}'.format(theme.back_color))
        print('danger_color: {}'.format(theme.danger_color))

@cli.command(help='Build theme packages')
@click.argument('names', nargs=-1)
def build(names):
    pkg_build(pkg_spec, names)

@cli.command(help='Clean building files')
@click.argument('names', nargs=-1)
def clean(names):
    if len(names) == 0:
        # clean build files of all of themes
        rm(pkg_spec.dest)
    else:
        # clean build files of specific themes
        names = [real_theme_name(name) for name in names[:]]
        for name in names:
            dest_theme = path.join(pkg_spec.dest, 'themes', name)
            rm(dest_theme)


@cli.command(help='Build, install to system and active it')
@click.argument('name')
def apply(name):
    name = real_theme_name(name)
    if name not in setting.themes:
        stdlog(stat_err, 'not found theme', name)
        sys.exit(1)

    dest_theme = path.join(setting.dest, 'themes', name)
    compile_theme(setting.src, dest_theme, setting.themes[name], pkg_config)
    stdlog(stat_done, 'compiled', name)

    if install_theme(name) != 0:
        stdlog(stat_err, 'install is not done', name)
    active_theme(name)

    stdlog(stat_done, 'applied', name)


@cli.command(help='Remove theme from system')
@click.argument('names', nargs=-1, required=True)
def remove(names):
    names = [real_theme_name(name) for name in names[:]]
    for name in names:
        remove_theme(name)


@cli.command(help='Clean all of build from system and try apply again')
@click.argument('name')
def use(name):
    if Popen([executable, 'ctl', 'remove', name]).wait() != 0:
        sys.exit(1)
    if Popen([executable, 'ctl', 'clean', name]).wait() != 0:
        sys.exit(1)
    if Popen([executable, 'ctl', 'build', name]).wait() != 0:
        sys.exit(1)
    if Popen([executable, 'ctl', 'apply', name]).wait() != 0:
        sys.exit(1)


@cli.command(help='Pack venom into package')
def dist():
    pkg_dist(pkg_spec)


@cli.command(help='Create new directory with file only in original directory')
@click.argument('odir')
@click.argument('sdir')
@click.argument('dest')
def dfile(odir, sdir, dest):
    diff_file(odir, sdir, dest)


@cli.command(help='Run unit testing')
def test():
    assert run_test() == 0


cli()
