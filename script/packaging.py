import os
import sys
import re
import shutil
from subprocess import Popen

from logger import stdlog, stat_done, stat_err


root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
_CLI_FILE = os.path.join(root, 'src', 'cli.sh')
_VERSION_RE = re.compile(r'VERSION="(.*)"')
_DEB_VERSION_RE = re.compile(r'DEB_VERSION="(.*)"')


def get_version():
    '''
    Get version of package from src/cli.sh

    :return: Dictionary contain two key 'version' and 'deb_version'
    :rtype: dict
    '''

    with open(_CLI_FILE, 'rb') as f:
        data = f.read()
        ver = _VERSION_RE.search(data).group(1)
        deb_ver = _DEB_VERSION_RE.search(data).group(1)

        return {'version': ver, 'deb_version': deb_ver}


def package_debian():
    src_metadata = os.path.join(root, 'src', 'pkg', 'DEBIAN', 'control')
    src_themes = os.path.join(root, 'dest')
    if not os.path.isdir(src_themes):
        stdlog(stat_err, 'not found builded files', src_themes)

    vers = get_version()
    pkg_ver = '{}-{}'.format(vers['version'], vers['deb_version'])
    pkg_name = 'venom_{}'.format(pkg_ver)
    dist_dir = os.path.join(root, 'dist')
    dist_pkg = os.path.join(dist_dir, pkg_name)
    dist_bin = os.path.join(dist_pkg, 'usr/bin')
    dist_metadata = os.path.join(dist_pkg, 'DEBIAN', 'control')
    dist_themes = os.path.join(dist_pkg, 'usr/share/themes')
    dist_icons = os.path.join(dist_pkg, 'usr/share/icons')

    # prepare file systems
    if os.path.isdir(dist_dir):
        shutil.rmtree(dist_dir, True)
    os.makedirs(os.path.dirname(dist_metadata))
    os.makedirs(dist_bin)
    os.makedirs(dist_themes)
    os.makedirs(dist_icons)

    # create meta data
    with open(src_metadata, 'r') as src_f:
        data = src_f.read().replace('{version}', pkg_ver)
        with open(dist_metadata, 'w') as dist_f:
            dist_f.write(data)

    # copy commandline
    src_cli = os.path.join(root, 'src/cli.sh')
    dist_cli = os.path.join(dist_bin, 'venom')
    shutil.copyfile(src_cli, dist_cli)
    if Popen(['chmod', '+x', dist_cli]).wait() != 0:
        stdlog(stat_err, 'chmod', dist_cli)
        sys.exit(1)

    # walk on directories of themes source and copy each theme to
    # package directory
    for theme_name in next(os.walk(src_themes))[1]:
        # copy theme files
        src_theme = os.path.join(src_themes, theme_name)
        target_theme = os.path.join(dist_themes, theme_name)
        ignore = shutil.ignore_patterns('icons')
        shutil.copytree(src_theme, target_theme, symlinks=True, ignore=ignore)
        stdlog(stat_done, 'theme copied', theme_name)

        # copy icon files
        src_icon = os.path.join(src_themes, theme_name, 'icons')
        target_icon = os.path.join(dist_icons, theme_name)
        shutil.copytree(src_icon, target_icon, symlinks=True)
        stdlog(stat_done, 'icon copied', theme_name)

    # build debian package
    if Popen(['dpkg-deb', '--build', '-D', dist_pkg, dist_dir]).wait() != 0:
        stdlog(stat_err, 'debian packed', pkg_name)
        sys.exit(1)

    # done
    stdlog(stat_done, 'debian packed', pkg_name)
