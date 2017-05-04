'''
SYNOPSIS

    build_theme(pkg_spec, theme_spec)

DESCRIPTION

    Build theme.

AUTHORS

    kevin leptons <kevin.leptons@gmail.com>
'''

import configparser
from os import path
from os.path import dirname

from .gtk_builder import build_gtk_theme
from .gnome_builder import build_gnome_theme
from .icon_builder import build_icon_theme
from .metacity_builder import build_metacity_theme
from .shell import cp, mkdir


def _build_config_file(pkg_spec, theme_spec):
    section = 'THEME'
    config_parser = configparser.RawConfigParser()
    config_parser.add_section(section)

    config_parser.set(section, 'front_color', theme_spec.front_color)
    config_parser.set(section, 'back_color', theme_spec.back_color)
    config_parser.set(section, 'danger_color', theme_spec.danger_color)

    dest_conf = path.join(pkg_spec.dest, 'themes', theme_spec.name,
                          'theme.conf')
    mkdir(dirname(dest_conf))
    f = open(dest_conf, 'w+')
    config_parser.write(f)
    f.close()


def build_theme(pkg_spec, theme_spec):
    # build congig file
    _build_config_file(pkg_spec, theme_spec)

    # build gtk theme
    build_gtk_theme(pkg_spec, theme_spec)

    # build gnome theme
    build_gnome_theme(pkg_spec, theme_spec)

    # build icon theme
    build_icon_theme(pkg_spec, theme_spec)

    # build metatcity theme
    build_metacity_theme(pkg_spec, theme_spec)

    # not thing will be build here
    # but gtk-2.0 directory must be exist to gnome shell
    # realize gtk3 themes
    gtk2_src = path.join(pkg_spec.src, 'gtk-2.0')
    gtk2_dest = path.join(pkg_spec.dest, 'themes', theme_spec.name, 'gtk-2.0')
    cp(gtk2_src, gtk2_dest)
