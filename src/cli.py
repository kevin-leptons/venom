#!/usr/bin/env python

import os
import sys
import ConfigParser

from subprocess import Popen


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
    config = ConfigParser.ConfigParser(default_config)
    config.read([theme_config])

    return ThemeConfig(
        config.get('THEME', 'front_color'),
        config.get('THEME', 'back_color'),
        config.get('THEME', 'danger_color')
    )


def print_help(exename):
    print 'USAGE'
    print '    {} active <name>'.format(exename)


def active_theme(name):
    config = read_config(name)

    # set background
    if config is not None:
        cmd_background = [
            'gsettings', 'set', 'org.gnome.desktop.background',
            'primary-color', '"{}"'.format(config.back_color)
        ]
        if Popen(cmd_background).wait() != 0:
            print 'error set background: {}'.format(config.back_color)
            sys.exit(1)

    # active GTK theme
    cmd_gtk = [
        'gsettings', 'set', 'org.gnome.desktop.interface',
        'gtk-theme', '"{}"'.format(name)
    ]
    if Popen(cmd_gtk).wait() != 0:
        print 'error active gtk theme: {}'.format(name)
        sys.exit(1)

    # active GNOME theme
    cmd_gnome = [
        'gsettings', 'set', 'org.gnome.shell.extensions.user-theme',
        'name', '"{}"'.format(name)
    ]
    if Popen(cmd_gnome).wait() != 0:
        print 'error active gnome theme: {}'.format(name)
        sys.exit(1)

    # active icons theme
    cmd_icon = [
        'gsettings', 'set', 'org.gnome.desktop.interface',
        'icon-theme', '"{}"'.format(name)
    ]
    if Popen(cmd_icon).wait() != 0:
        print 'error active icon theme: {}'.format(name)
        sys.exit(1)

    # active window theme. it is also called metacity theme
    cmd_metacity = [
        'gsettings', 'set', 'org.gnome.desktop.wm.preferences',
        'theme', '"{}"'.format(name)
    ]
    if Popen(cmd_metacity).wait() != 0:
        print 'error active metacity: {}'.format(name)
        sys.exit(1)


def cli():
    exename = sys.argv[0]

    if len(sys.argv) != 3:
        print_help(exename)
        sys.exit(1)
    elif sys.argv[1] == 'active':
        theme_name = sys.argv[2]
        if not os.path.isdir('/usr/share/themes/{}'.format(theme_name)):
            print 'error theme not found: {}'.format(theme_name)
            sys.exit(1)

        sys.exit(active_theme(theme_name))
    else:
        print_help(exename)
        sys.exit(1)


cli()
