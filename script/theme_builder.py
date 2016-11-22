import os
import dirsync

from .gtk_builder import compile_gtk
from .gnome_builder import compile_gnome
from .icon_builder import compile_icon
from .metacity_builder import compile_metacity


def compile_theme(src, dest, config):
    '''
    Compile GTK theme. Theme after compiled will contains
        - GTK3 theme
        - GNOME shell theme
        - Icon theme

    :param str src: Source directory. It must 'src' directory, contains
        resources to build theme
    :param str dest: Destination directory
    :param ThemeConfig: Configuration of theme
    '''

    gtk3_src = '{}/gtk-3.0'.format(src)
    gtk3_dest = '{}/gtk-3.0'.format(dest)
    compile_gtk(gtk3_src, gtk3_dest, config)

    gnome_src = '{}/gnome-shell'.format(src)
    gnome_dest = '{}/gnome-shell'.format(dest)
    compile_gnome(gnome_src, gnome_dest, config)

    icon_src = '{}/icons'.format(src)
    icon_dest = '{}/icons'.format(dest)
    compile_icon(icon_src, icon_dest, config)

    metacity_src = '{}/metacity-1'.format(src)
    metacity_dest = '{}/metacity-1'.format(dest)
    compile_metacity(metacity_src, metacity_dest, config)

    # must have gtk-2.0 directory to theme engine realize all of GTK themes
    gtk2_src = '{}/gtk-2.0'.format(src)
    gtk2_dest = '{}/gtk-2.0'.format(dest)
    if not os.path.isdir(gtk2_dest):
        os.makedirs(gtk2_dest)
    dirsync.sync(gtk2_src, gtk2_dest, 'sync', create=True)
