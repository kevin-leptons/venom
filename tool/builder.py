'''
SYNOPSIS

    pkg_build(spec)
    pkg_build_clean(spec)
    pkg_dist(spec)
    pkg_dist_clean(spec)
    list_theme()

DESCRIPTION

    Building functions.

AUTHORS

    Kevin Leptons <kevin.leptons@gmail.com>
'''

from os import path
from collections import OrderedDict

from .error import ThemeNotSpecifyError
from .man_builder import build_manpage
from .theme_builder import build_theme
from .packaging import pack_debian
from .util import real_theme_name
from .shell import rm
from .types import ThemeSpec

_THEME_SPECS = OrderedDict([
    ('venom-black', ThemeSpec('venom-black', '#000000', '#fefefe', 'red')),
    ('venom-orange', ThemeSpec('venom-orange', '#ff8c00', 'black', 'red')),
    ('venom-green', ThemeSpec('venom-green', '#55af66', 'black', 'red')),
])


def pkg_build_clean(spec, theme_names):
    if len(theme_names) == 0:
        # clean all of build files
        rm(spec.dest)
    else:
        # clean build file of specific theme
        real_names = [real_theme_name(name) for name in theme_names]
        for name in real_names:
            theme_spec = _THEME_SPECS[name]
            rm(path.join(spec.dest, 'themes', theme_spec.name))


def pkg_build(spec, theme_names):
    # build man page
    build_manpage(spec)

    # build all of themes
    if len(theme_names) == 0:
        for name in _THEME_SPECS:
            build_theme(spec, _THEME_SPECS[name])
    else:
        # build themes was specify
        names = [real_theme_name(name) for name in theme_names[:]]
        for name in names:
            if name not in _THEME_SPECS:
                raise ThemeNotSpecifyError(name)
            build_theme(spec, _THEME_SPECS[name])


def pkg_dist_clean(spec):
    rm(spec.dist)


def pkg_dist(spec):
    pack_debian(spec)


def list_theme():
    for name in _THEME_SPECS:
        theme_spec = _THEME_SPECS[name]
        msg = '{}, fcolor={}, bcolor={}, dcolor={}'.format(
              theme_spec.name, theme_spec.front_color,
              theme_spec.back_color, theme_spec.danger_color)
        print(msg)
