import os
import sys
import ConfigParser

from subprocess import Popen

from error import ThemeNotFoundError
from theme_config import ThemeConfig


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
        name,
        config.get('THEME', 'front_color'),
        config.get('THEME', 'back_color'),
        config.get('THEME', 'danger_color')
    )


def set_theme(name):
    config = read_config(name)

    # set background
    if config is not None:
        cmd_bg = [
            'gsettings', 'set', 'org.gnome.desktop.background',
            'primary-color', '"{}"'.format(config.back_color)
        ]
        if Popen(cmd_bg).wait() != 0:
            print 'error set bg primary: {}'.format(config.back_color)
            sys.exit(1)
        cmd_bg_shade = [
            'gsettings', 'set', 'org.gnome.desktop.background',
            'color-shading-type', 'solid'
        ]
        if Popen(cmd_bg_shade).wait() != 0:
            print 'error set bg shade: solid'
            sys.exit(1)
        cmd_bg_img = [
            'gsettings', 'set', 'org.gnome.desktop.background',
            'picture-uri', ''
        ]
        if Popen(cmd_bg_img).wait() != 0:
            print 'error set background uri: ""'
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


def active_theme(name):
    '''
    Apply theme use command line, contains
        - GTK theme
        - GNOME theme
        - Icons theme

    Priority: ~/.themes; ~/.local/share/themes; /usr/share/themes

    But it not ensure that theme is activated or not. Because command line
    does not inform any things. Best behavior is search theme on variant
    directory and raise error if no one is exist

    :param str: Name of theme
    :raise ThemeNotFoundError: On theme not found
    '''

    # find theme on ~/.themes/<name> directory
    usr_theme = '~/.themes/{}'.format(name)
    if not os.path.isdir(usr_theme):
        set_theme(name)
        return

    # find theme on ~/.local/share/themes/<name>
    usr_local_theme = '~/.local/share/themes/{}'.format(name)
    if not os.path.isdir(usr_local_theme):
        set_theme(name)
        return

    # find theme on /usr/share/themes/<name>
    global_theme = '/usr/share/themes/{}'.format(name)
    if not os.path.isdir(global_theme):
        set_theme(name)
        return

    # not found theme in any where
    raise ThemeNotFoundError(name)
