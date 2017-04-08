'''
SPEC    : Use to compile one theme

EXPORT  : compile_theme()

AUTHOR  : kevin leptons <kevin.leptons@gmail.com>
'''

import os
import dirsync

from os import path

from .config_builder import compile_config
from .gtk_builder import compile_gtk
from .gnome_builder import compile_gnome
from .icon_builder import compile_icon
from .metacity_builder import compile_metacity


def compile_theme(src, dest, config, pkg_config):
    '''
    Compile theme, includes:
        - GTK3 theme
        - GNOME shell theme
        - Icon theme
        - Metacity theme

    :param str src: Path to directory contains asset of theme
    :param str dest: Path to destination directory to store result
    :param ThemeConfig: Configuration of theme
    :param PackageConfig: Configuration of package
    '''

    # create congig file
    compile_config(src, dest, config)

    # build gtk theme
    gtk3_src = path.join(src, 'gtk-3.0')
    gtk3_dest = path.join(dest, 'gtk-3.0')
    compile_gtk(gtk3_src, gtk3_dest, config, pkg_config)

    # build gnome theme
    gnome_src = path.join(src, 'gnome-shell')
    gnome_dest = path.join(dest, 'gnome-shell')
    compile_gnome(gnome_src, gnome_dest, config, pkg_config)

    # build icon theme
    icon_src = path.join(src, 'icons')
    icon_dest = path.join(dest, 'icons')
    compile_icon(icon_src, icon_dest, config, pkg_config)

    # build metatcity theme
    metacity_src = path.join(src, 'metacity-1')
    metacity_dest = path.join(dest, 'metacity-1')
    compile_metacity(metacity_src, metacity_dest, config)

    # not thing will be build here
    # but gtk-2.0 directory must be exist to theme engine
    # realize gtk3 themes
    gtk2_src = path.join(src, 'gtk-2.0')
    gtk2_dest = path.join(dest, 'gtk-2.0')
    if not os.path.isdir(gtk2_dest):
        os.makedirs(gtk2_dest)
    dirsync.sync(gtk2_src, gtk2_dest, 'sync', create=True)
