#!/usr/bin/env python

# DESCRIPTIONS
#
# Apply theme use command line, contains
#    - GTK theme
#    - GNOME theme
#    - Icons theme
#
# But it not ensure that theme is activated or not. Because command line
# does not inform any things. Best behavior is search theme on variant
# directory and raise error if no one is exist
#
# USAGE
#
# $ venom active <name>
#
# AUTHOR: kevin leptons <kevin.leptons@gmail.com>

import os
import sys
import ConfigParser

from subprocess import Popen

VERSION = "0.0.3"
DEB_VERSION = "0"

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
    print '    {} active <name>     active theme'.format(exename)
    print '    {} -v, --version     print version'.format(exename)
    print '    {} -h, --help        print help'.format(exename)


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
            return 1

    # active GTK theme
    cmd_gtk = [
        'gsettings', 'set', 'org.gnome.desktop.interface',
        'gtk-theme', '"{}"'.format(name)
    ]
    if Popen(cmd_gtk).wait() != 0:
        print 'error active gtk theme: {}'.format(name)
        return 1

    # active GNOME theme
    cmd_gnome = [
        'gsettings', 'set', 'org.gnome.shell.extensions.user-theme',
        'name', '"{}"'.format(name)
    ]
    if Popen(cmd_gnome).wait() != 0:
        print 'error active gnome theme: {}'.format(name)
        return 1

    # active icons theme
    cmd_icon = [
        'gsettings', 'set', 'org.gnome.desktop.interface',
        'icon-theme', '"{}"'.format(name)
    ]
    if Popen(cmd_icon).wait() != 0:
        print 'error active icon theme: {}'.format(name)
        return 1

    # active window theme. it is also called metacity theme
    cmd_metacity = [
        'gsettings', 'set', 'org.gnome.desktop.wm.preferences',
        'theme', '"{}"'.format(name)
    ]
    if Popen(cmd_metacity).wait() != 0:
        print 'error active metacity: {}'.format(name)
        return 1

    return 0


def cli():
    exename = os.path.basename(sys.argv[0])

    if len(sys.argv) < 2:
        print_help(exename)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == 'active':
        if len(sys.argv) != 3:
            print_help(exename)
            sys.exit(1)

        theme_name = sys.argv[2]
        if not os.path.isdir('/usr/share/themes/{}'.format(theme_name)):
            print 'error theme not found: {}'.format(theme_name)
            sys.exit(1)

        sys.exit(active_theme(theme_name))
    elif cmd == '-v' or cmd == '--version':
        print 'venom v{}'.format(VERSION)
    elif cmd == '-h' or cmd == '--help':
        print_help(exename)
    else:
        print_help(exename)
        sys.exit(1)


cli()
