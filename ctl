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
    # build GOB theme
    mkdir -vp $DEST_GOB_GTK3
    cp -rv $SRC/gob-index.theme $DEST_GOB/index.theme
    bundle exec sass $SRC_GOB_GTK3/gtk-gob.scss $DEST_GOB_GTK3/gtk.css
    mkdir -vp $DEST_GOB_GTK2
    rsync -rv $SRC_GNOME/* $DEST_GOB_GNOME --exclude=*.swp
    rsync -rv $SRC_METACITY/* $DEST_GOB_METACITY --exclude=*.swp

    # build BOW theme
    mkdir -vp $DEST_BOW_GTK3
    cp -rv $SRC/bow-index.theme $DEST_BOW/index.theme
    bundle exec sass $SRC_BOW_GTK3/gtk-bow.scss $DEST_BOW_GTK3/gtk.css
    mkdir -vp $DEST_BOW_GTK2
    rsync -rv $SRC_GNOME/* $DEST_BOW_GNOME --exclude=*.swp
    rsync -rv $SRC_METACITY/* $DEST_BOW_METACITY --exclude=*.swp
}

repo_install()
{
    repo_build

    # install GOB theme
    sudo mkdir -vp $TARGET_GOB
    sudo cp -rv $DEST_GOB/* $TARGET_GOB

    # install BOW theme
    sudo mkdir -vp $TARGET_BOW
    sudo cp -rv $DEST_BOW/* $TARGET_BOW

    # gnome-tweak-tool
    gtk3-widget-factory
}

repo_clean()
{
    rm -rf $DEST
}

repo_remove()
{
    sudo rm -rf $TARGET_GOB
    sudo rm -rf $TARGET_BOW
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
