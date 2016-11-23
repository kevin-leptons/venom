#!/bin/bash

# Use as tool to active GNOME theme
#
# AUTHOR: kevin leptons <kevin.leptons@gmail.com>
#

set -e

VERSION="0.0.1"
DEB_VERSION="0"

# help menu
HELP="USAGE:\n
    $(basename $0) active <name>    active theme by name
    $(basename $0) -v               print version
    $(basename $0) -h               print help menu\n"

# DESCRIPTIONS
#
# Set GTK theme, GNOME shell, Icon and Metatcity of system
#
# USAGE
#
# $ set_theme <name>
#
set_theme() {
    local NAME="$1"
    if [ -z "${NAME// }" ]; then
        echo "name argument is required"
        return 1
    fi

    # active GTK theme
    gsettings set org.gnome.desktop.interface gtk-theme "$NAME"

    # active GNOME theme
    gsettings set org.gnome.shell.extensions.user-theme name "$NAME"

    # active icons theme
    gsettings set org.gnome.desktop.interface icon-theme name

    # active window theme. it is also called metacity theme
    gsettings set org.gnome.desktop.wm.preferences theme "$NAME"
}

#
# DESCRIPTIONS
#
# Apply theme use command line, contains
#    - GTK theme
#    - GNOME theme
#    - Icons theme
#
# Priority: ~/.themes; ~/.local/share/themes; /usr/share/themes
#
# But it not ensure that theme is activated or not. Because command line
# does not inform any things. Best behavior is search theme on variant
# directory and raise error if no one is exist
#
# USAGE
#
# $ active_theme <name>
#
active_theme() {
    local NAME="$1"
    if [ -z "${NAME// }" ]; then
        echo "name argument is required"
        return 1
    fi

    # find theme on ~/.themes/<name> directory
    local USR_THEME="$HOME/.theme/$NAME"
    if [ -d "$USR_THEME" ]; then
        set_theme "$NAME"
        exit 0
    fi

    # find theme on ~/.local/share/themes/<name>
    local USR_LOCAL_THEME="$HOME/.local/share/themes/$NAME"
    if [ -d "$USR_LOCAL_THEME" ]; then
        set_theme "$NAME"
        exit 0
    fi

    # find theme on /usr/share/themes/<name>
    local USR_SHARE_THEME="/usr/share/themes/$NAME"
    if [ -d "$USR_SHARE_THEME" ]; then
        set_theme "$NAME"
        exit 0
    fi

    # not found theme in any where
    echo "not found theme: $NAME"
    exit 1
}

print_version() {
    echo "venom v$VERSION-$DEB_VERSION"
}

print_help() {
    printf "$HELP"
}

# parse arguments and execute command
case "$1" in
    active) active_theme "$2"; exit 0;;
    -v) print_version; exit 0;;
    -h) print_help; exit 0;;
    *) print_help; exit 1;;
esac
