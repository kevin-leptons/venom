import os
import re


root = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
_CLI_FILE = os.path.join(root, 'src', 'cli.py')
_VERSION_RE = re.compile(r'VERSION = "(.*)"')
_DEB_VERSION_RE = re.compile(r'DEB_VERSION = "(.*)"')


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
