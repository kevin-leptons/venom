#!/bin/bash

# SPEC      : controller of repository
# AUTHOR    : kevin leptons <kevin.leptons@gmail.com>

# bash options
set -e

# variables
ROOT=$(realpath .)

SRC="$ROOT/src"
DEST="$ROOT/dest"
TARGET="/usr/share/themes"

# share for both GOB and BOW theme
SRC_GNOME="$SRC/gnome-shell"
SRC_METACITY="$SRC/metacity-1"

# green on black theme
SRC_GOB_GTK3="$SRC/gtk-3.0"

DEST_GOB="$DEST/venom-gob"
DEST_GOB_GTK2="$DEST_GOB/gtk-2.0"
DEST_GOB_GTK3="$DEST_GOB/gtk-3.0"
DEST_GOB_GNOME="$DEST_GOB/gnome-shell"
DEST_GOB_METACITY="$DEST_GOB/metacity-1"

TARGET_GOB="$TARGET/venom-gob"

# black on white theme
SRC_BOW_GTK3="$SRC/gtk-3.0"

DEST_BOW="$DEST/venom-bow"
DEST_BOW_GTK2="$DEST_BOW/gtk-2.0"
DEST_BOW_GTK3="$DEST_BOW/gtk-3.0"
DEST_BOW_GNOME="$DEST_BOW/gnome-shell"
DEST_BOW_METACITY="$DEST_BOW/metacity-1"

TARGET_BOW="$TARGET/venom-bow"


# help menu
HELP="USAGE:\n
    $(basename $0) build        build repo
    $(basename $0) install      install repo to system
    $(basename $0) clean        clean build
    $(basename $0) remove       remove repo from system
    $(basename $0) -h           show help menu"

repo_build()
{
    ./builder.py build --name venom-green \
        --front-color "#55af66" --back-color black --danger-color orange
    ./builder.py build --name venom-orange \
        --front-color "#ff8c00" --back-color black --danger-color orange
    ./builder.py build --name venom-teal \
        --front-color "#008080" --back-color black --danger-color orange
}

install_theme()
{
    local NAME="$1"

    sudo mkdir -vp "/usr/share/themes/$NAME"
    sudo cp -r dest/$NAME/* "/usr/share/themes/$NAME"

    sudo mkdir -vp "/usr/share/icons/$NAME"
    sudo cp -r dest/$NAME/icons/* "/usr/share/icons/$NAME"
}

active_theme()
{
    local NAME="$1"

    gsettings set org.gnome.desktop.interface gtk-theme "$NAME"
    gsettings set org.gnome.shell.extensions.user-theme name "$NAME"
    gsettings set org.gnome.desktop.interface icon-theme "$NAME"
    gsettings set org.gnome.desktop.wm.preferences theme "$NAME"

    gsettings set org.gnome.desktop.background primary-color "#000000"
}

repo_install()
{
    install_theme "venom-green"
    install_theme "venom-orange"
    install_theme "venom-teal"
}

repo_clean()
{
    rm -rf $DEST
    echo "removed $DEST"
}

repo_remove()
{
    sudo rm -rf $TARGET_GOB
    echo "removed $TARGET_GOB"

    sudo rm -rf $TARGET_BOW
    echo "removed $TARGET_BOW"
}

show_help()
{
    printf "$HELP"
}

# parse arguments
case "$1" in
    build) repo_build; exit 0;;
    install) repo_install; exit 0;;
    clean) repo_clean; exit 0;;
    remove) repo_remove; exit 0;;
    active) active_theme "$2"; exit 0;;
    -h) show_help; exit 0;;
    *) show_help; exit 1;;
esac
