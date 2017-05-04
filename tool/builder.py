'''
SYNOPSIS

    class Version
    class PkgSpec

    pkg_build(spec)
    pkg_dist(spec)

DESCRIPTION

    Building functions.

AUTHORS

    Kevin Leptons <kevin.leptons@gmail.com>
'''

from .error import ThemeNotSpecifyError
from .theme_spec import THEME_SPECS
from .man_builder import build_manpage
from .theme_builder import build_theme
from .packaging import pack_debian
from .util import real_theme_name


class Version:
    def __init__(self, major, minor, rev=0, deb_rev=0):
        self._major = major
        self._minor = minor
        self._rev = rev
        self._pkg_ver = '{}.{}.{}'.format(major, minor, rev)
        self._deb_rev = deb_rev
        self._deb_ver = '{}-{}'.format(self._pkg_ver, deb_rev)

    @property
    def major(self):
        return self._major

    @property
    def minor(self):
        return self._minor

    @property
    def rev(self):
        return self._rev

    @property
    def pkg_ver(self):
        return self._pkg_ver

    @property
    def deb_rev(self):
        return self._deb_rev

    @property
    def deb_ver(self):
        return self._deb_ver


class PkgSpec:
    def __init__(self, name, version, root, src, dest, dist, test):
        self._name = name
        self._deb_name = '{}_{}'.format(name, version.deb_ver)
        self._version = version
        self._root = root
        self._src = src
        self._dest = dest
        self._dist = dist
        self._test = test

    @property
    def name(self):
        return self._name

    @property
    def deb_name(self):
        return self._deb_name

    @property
    def version(self):
        return self._version

    @property
    def root(self):
        return self._root

    @property
    def src(self):
        return self._src

    @property
    def dest(self):
        return self._dest

    @property
    def dist(self):
        return self._dist

    @property
    def test(self):
        return self._test


def pkg_build(spec, theme_names):
    # build man page
    build_manpage(spec)

    # build all of themes
    if len(theme_names) == 0:
        for name in THEME_SPECS:
            build_theme(spec, THEME_SPECS[name])
    else:
        # build themes was specify
        names = [real_theme_name(name) for name in theme_names[:]]
        for name in names:
            if name not in THEME_SPECS:
                raise ThemeNotSpecifyError(name)
            build_theme(spec, THEME_SPECS[name])


def pkg_dist(spec):
    pack_debian(spec)
