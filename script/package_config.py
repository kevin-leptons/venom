'''
SPEC    : Specify package configuration

EXPORT  : PackageConfig()

AUTHOR  : kevin leptons <kevin.leptons@gmail.com>
'''


class PackageConfig(object):
    '''
    Configuration of theme. Use by compiler

    :param str name: Name of package
    :param str src: Path to source directory
    :param str dest: Path to destination directory
    '''

    def __init__(self, name, src, dest):
        self._name = name
        self._src = src
        self._dest = dest

    @property
    def name(self):
        return self._name

    @property
    def src(self):
        return self._src

    @property
    def dest(self):
        return self._dest
