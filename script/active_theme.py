import os
from subprocess import Popen

from error import ThemeNotFoundError


def set_theme(name):
    # active GTK theme
    Popen([
        'gsettings', 'set', 'org.gnome.desktop.interface',
        'gtk-theme', name]
    ).wait()

    # active GNOME theme
    Popen([
        'gsettings', 'set', 'org.gnome.shell.extensions.user-theme',
        'name', name]
    ).wait()

    # active icons theme
    Popen([
        'gsettings', 'set', 'org.gnome.desktop.interface', 'icon-theme',
        name]
    ).wait()

    # active window theme. it is also called metacity theme
    Popen([
        'gsettings', 'set', 'org.gnome.desktop.wm.preferences',
        'theme', name]
    ).wait()

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
