'''
SPEC    : Use to build GTK3 theme

EXPORT  : compile_gtk()

AUTHOR  : kevin leptons <kevin.leptons@gmail.com>
'''

from os import path

from .sass_builder import compile_sass
from .icon_converter import convert_icon


def compile_gtk(src, dest, config, pkg_config):
    '''
    Compile GTK3 theme. Compile will asset in src directory, build by config
    then store result in dest directory

    :param str src: Directory contains asset of GTK3 theme
    :param str dest: Directory to store result
    :param ThemeConfig config: Theme's configuration
    :param PackageConfig config: Package's configuration
    '''

    # compile scss
    src_scss = '{}/gtk.scss'.format(src)
    dest_scss = '{}/gtk.css'.format(dest)
    sass_vars = {
        'front_color': config.front_color,
        'back_color': config.back_color,
        'danger_color': config.danger_color
    }
    compile_sass(src_scss, dest_scss, sass_vars)

    # compile asset
    icon_src = path.join(src, 'asset')
    icon_dest = path.join(dest, 'asset')
    convert_icon(icon_src, icon_dest, config)
