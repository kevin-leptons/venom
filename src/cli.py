#!/usr/bin/env python3

'''
SYNOPSIS

    <cmd> list theme
    <cmd> use <name>
    <cmd> -v, --version
    <cmd> -h, --help

DESCRIPTIONS

    *list* show all of theme's names.

    *use <name>* active theme by theme's name. Theme's names are list
    by *list theme*.

EXAMPLES

    $ venom use black

AUTHORS

    Kevin Leptons <kevin.leptons@gmail.com>
'''

import os
import sys
import configparser
from os import path
from os.path import isdir
from subprocess import Popen, CalledProcessError
from gi.repository import Gio

VERSION = "maj.min.rev"
DEB_VERSION = "0"
DEF_THEME_NAME = 'Adwaita'
DEF_ICON_NAME = 'gnome'
DEF_SHELL_NAME = ''
DEF_BACKGROUND_COLOR = '#ffffff'
_GEXT_USER_THEME = 'user-theme@gnome-shell-extensions.gcampax.github.com'
_ENABLED_EXTENSIONS_KEY = 'enabled-extensions'


class ThemeNotFoundError(Exception):
    def __init__(self, path):
        self._path = path

    def __str__(self):
        return self._path


def call(args, cwd=None):
    exit_code = Popen(args, cwd=cwd).wait()
    if exit_code != 0:
        raise CalledProcessError(exit_code, args)


def real_theme_name(short_name):
    return 'venom-{}'.format(short_name)


class ThemeConfig(object):
    def __init__(self, front_color, back_color, danger_color):
        self._front_color = front_color
        self._back_color = back_color
        self._danger_color = danger_color

    @property
    def front_color(self):
        return self._front_color

    @property
    def back_color(self):
        return self._back_color

    @property
    def danger_color(self):
        return self._danger_color


def read_config(name):
    theme_config = '/usr/share/themes/{}/theme.conf'.format(name)
    if not os.path.isfile(theme_config):
        return None

    default_config = {
        'front_color': '#55af66',
        'back_color': '#000000',
        'danger_color': '#ff0000'
    }
    config = configparser.ConfigParser(default_config)
    config.read([theme_config])

    return ThemeConfig(
        config.get('THEME', 'front_color'),
        config.get('THEME', 'back_color'),
        config.get('THEME', 'danger_color')
    )


def print_help(exename):
    print('USAGE')
    print('    {} list              list them name'.format(exename))
    print('    {} use <name>        active theme'.format(exename))
    print('    {} -v, --version     print version'.format(exename))
    print('    {} -h, --help        print help'.format(exename))


def cmd_list():
    names = ['default', 'black', 'green', 'orange']
    for name in names:
        print(name)


def enable_gnome_extension(name):
    settings = Gio.Settings(schema='org.gnome.shell')
    extensions = settings.get_strv(_ENABLED_EXTENSIONS_KEY)

    if name in extensions:
        return

    extensions.append(name)
    settings.set_strv(_ENABLED_EXTENSIONS_KEY, extensions)


def active_theme(name):
    theme_dir = path.join('/usr/share/themes', name)
    if not isdir(theme_dir):
        raise ThemeNotFoundError(theme_dir)

    config = read_config(name)

    # enable user-theme extension
    enable_gnome_extension(_GEXT_USER_THEME)

    # background
    cmd_bg_shade = [
        'gsettings', 'set', 'org.gnome.desktop.background',
        'color-shading-type', 'solid'
    ]
    call(cmd_bg_shade)
    if config is None:
        # theme configuration not found, it isn't venom theme
        # use default solid background
        cmd_bg = [
            'gsettings', 'set', 'org.gnome.desktop.background',
            'primary-color', '"{}"'.format(DEF_BACKGROUND_COLOR)
        ]
        call(cmd_bg)
    else:
        # them configuration was found, it's venom theme
        # use venom image as background
        cmd_bg = [
            'gsettings', 'set', 'org.gnome.desktop.background',
            'primary-color', '"{}"'.format(config.back_color)
        ]
        call(cmd_bg)

        wallpaper = path.join('/usr/share/themes', name,
                              'gtk-3.0/asset/venom-wallpaper.svg')
        cmd_bg_img = [
            'gsettings', 'set', 'org.gnome.desktop.background',
            'picture-uri', wallpaper
        ]
        call(cmd_bg_img)

    # active GTK theme
    cmd_gtk = [
        'gsettings', 'set', 'org.gnome.desktop.interface',
        'gtk-theme', '"{}"'.format(name)
    ]
    call(cmd_gtk)

    # active GNOME theme
    shell_name = name
    if name == DEF_THEME_NAME:
        shell_name = DEF_SHELL_NAME
    cmd_gnome = [
        'gsettings', 'set', 'org.gnome.shell.extensions.user-theme',
        'name', '"{}"'.format(shell_name)
    ]
    call(cmd_gnome)

    # active icons theme
    icon_name = name
    if name == DEF_THEME_NAME:
        icon_name = DEF_ICON_NAME
    cmd_icon = [
        'gsettings', 'set', 'org.gnome.desktop.interface',
        'icon-theme', '"{}"'.format(icon_name)
    ]
    call(cmd_icon)

    # active window theme. it is also called metacity theme
    cmd_metacity = [
        'gsettings', 'set', 'org.gnome.desktop.wm.preferences',
        'theme', '"{}"'.format(name)
    ]
    call(cmd_metacity)


def cli():
    exename = os.path.basename(sys.argv[0])

    # not match with any commands
    if len(sys.argv) < 2:
        print_help(exename)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'list':
        cmd_list()
    elif cmd == 'use':
        if len(sys.argv) != 3:
            print_help(exename)
            sys.exit(1)

        if sys.argv[2] == 'default':
            active_theme(DEF_THEME_NAME)
        else:
            active_theme(real_theme_name(sys.argv[2]))
    elif cmd == '-v' or cmd == '--version':
        print('venom v{}'.format(VERSION))
    elif cmd == '-h' or cmd == '--help':
        print_help(exename)
    else:
        print_help(exename)
        sys.exit(1)


cli()
