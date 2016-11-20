#!/bin/bash

# SPEC      : controller of repository
# AUTHOR    : kevin leptons <kevin.leptons@gmail.com>

# bash options
set -e

# variables
ROOT=$(realpath .)

SRC="$ROOT/src"
SRC_GTK3="$SRC/gtk-3.0"
SRC_GNOME="$SRC/gnome-shell"
SRC_METACITY="$SRC/metacity-1"

DEST="$ROOT/dest"
DEST_GTK2="$DEST/gtk-2.0"
DEST_GTK3="$DEST/gtk-3.0"
DEST_GNOME="$DEST/gnome-shell"
DEST_METACITY="$DEST/metacity-1"

TARGET="/usr/share/themes/venom"

# help menu
HELP="USAGE:\n
    $(basename $0) build        build repo
    $(basename $0) install      install repo to system
    $(basename $0) clean        clean build
    $(basename $0) remove       remove repo from system
    $(basename $0) -h           show help menu"

repo_build()
{
    mkdir -vp $DEST_GTK3
    cp -rv $SRC/index.theme $DEST/index.theme

    bundle exec sass $SRC_GTK3/gtk.scss $DEST_GTK3/gtk.css

    mkdir -vp $DEST_GTK2

    rsync -rv $SRC_GNOME/* $DEST_GNOME --exclude=*.swp

    rsync -rv $SRC_METACITY/* $DEST_METACITY --exclude=*.swp
}

repo_install()
{
    repo_build

    sudo mkdir -vp $TARGET
    sudo rsync -rv $DEST/* $TARGET --exclude=*.swp
    gtk3-widget-factory
    # gnome-tweak-tool
}

repo_clean()
{
    rm -rf $DEST
}

repo_remove()
{
    sudo rm -rf $TARGET
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
    -h) show_help; exit 0;;
    *) show_help; exit 1;;
esac
