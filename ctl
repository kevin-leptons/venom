#!/usr/bin/env python

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

from script.logger import stdlog, stat_done, stat_err
from script import compile_theme, install_theme, active_theme, remove_theme, \
                   package_debian, diff_file, compile_manpage
from script.util import real_theme_name, short_theme_name
from script.test import run_test

import setting


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
            print short_theme_name(name)
    else:
        # list properties of theme

        name = real_theme_name(name)
        if name not in themes:
            stdlog(stat_err, 'not found theme', name)
            sys.exit(1)

        theme = themes[name]
        print 'name: {}'.format(short_theme_name(name))
        print 'front_color: {}'.format(theme.front_color)
        print 'back_color: {}'.format(theme.back_color)
        print 'danger_color: {}'.format(theme.danger_color)

@cli.command(help='Build theme packages')
@click.argument('names', nargs=-1)
def build(names):
    themes = setting.themes
    src = setting.src
    dest = os.path.join(setting.dest, 'themes')

    # create man page
    man_src = os.path.join(src, 'man')
    man_dest = os.path.join(setting.dest, 'man')
    compile_manpage(man_src, man_dest)

    if len(names) == 0:
        # build all of themes
        for name in themes:
            dest_theme = '{}/{}'.format(dest, themes[name].name)
            compile_theme(src, dest_theme, themes[name])
        for name in themes:
            stdlog(stat_done, 'compiled', name)
    else:
        # build only theme was specify
        names = [real_theme_name(name) for name in names[:]]
        for name in names:
            if name not in themes:
                stdlog(stat_err, 'not found theme', name)
                sys.exit(1)

            dest_theme = '{}/{}'.format(dest, name)
            compile_theme(src, dest_theme, themes[name])

        for name in names:
            stdlog(stat_done, 'compiled', name)

@cli.command(help='Clean building files')
@click.argument('names', nargs=-1)
def clean(names):
    if len(names) == 0:
        # clean build files of all of themes
        if os.path.isdir(setting.dest):
            shutil.rmtree(setting.dest)
        stdlog(stat_done, 'clean dest', setting.dest)

    else:
        # clean build files of specific themes
        names = [real_theme_name(name) for name in names[:]]
        for name in names:
            dest_theme = path.join(setting.dest, 'themes', name)
            if os.path.isdir(dest_theme):
                shutil.rmtree(dest_theme)

        for name in names:
            stdlog(stat_done, 'clean dest', name)


@cli.command(help='Build, install to system and active it')
@click.argument('name')
def apply(name):
    name = real_theme_name(name)
    if name not in setting.themes:
        stdlog(stat_err, 'not found theme', name)
        sys.exit(1)

    dest_theme = path.join(setting.dest, 'themes', name)
    compile_theme(setting.src, dest_theme, setting.themes[name])
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


@cli.command(help='Package venom themes into package')
def dist():
    package_debian()


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
