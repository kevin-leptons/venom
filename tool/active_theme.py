'''
SPEC    : Use to active theme on system

EXPORT  : active_theme()

AUTHOR  : kevin leptons <kevin.leptons@gmail.com>
'''

import configparser
from os import path
from os.path import isdir, isfile

from .error import ThemeNotFoundError
from .theme_config import ThemeConfig
from .shell import call

DEF_THEME_NAME = 'Adwaita'
DEF_ICON_NAME = 'gnome'
DEF_SHELL_NAME = ''
DEF_BACKGROUND_COLOR = '#ffffff'


def _read_config(name):
    theme_config = path.join('/usr/share/themes', name, 'theme.conf')
    if not isfile(theme_config):
        return None

    default_config = {
        'front_color': '#55af66',
        'back_color': '#000000',
        'danger_color': '#ff0000'
    }
    config = configparser.ConfigParser(default_config)
    config.read([theme_config])

    return ThemeConfig(
        name,
        config.get('THEME', 'front_color'),
        config.get('THEME', 'back_color'),
        config.get('THEME', 'danger_color')
    )


def active_theme(name):
    theme_dir = path.join('/usr/share/themes', name)
    if not isdir(theme_dir):
        raise ThemeNotFoundError(theme_dir)

    config = _read_config(name)

    if config is None:
        # theme configuration not found, it isn't venom theme
        # use default solid background color instead of image
        cmd_bg = [
            'gsettings', 'set', 'org.gnome.desktop.background',
            'primary-color', '"{}"'.format(DEF_BACKGROUND_COLOR)
        ]
        call(cmd_bg)

        cmd_bg_shade = [
            'gsettings', 'set', 'org.gnome.desktop.background',
            'color-shading-type', 'solid'
        ]
        call(cmd_bg_shade)
    else:
        # them configuration was found, it's venom theme
        # use venom image as background
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
    print(icon_name)
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
