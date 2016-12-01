'''
SPEC    : Use to build gnome theme

EXPORT  : compile_gnome()

AUTHOR  : kevin leptons <kevin.leptons@gmail.com>
'''

from .sass_builder import compile_sass
from .icon_builder import compile_icon


def compile_gnome(src, dest, config):
    '''
    Compile gnome-shell theme from. All of asset store in src directory,
    compiler will read, build by config. Then store result in dest directory

    :param str src: Directory contains asset of gnome-shell
    :param str dest: Directory to store result
    :param ThemeConfig config: Theme configuration
    '''

    # compile gnome-shell scss
    src_scss = '{}/gnome-shell.scss'.format(src)
    dest_css = '{}/gnome-shell.css'.format(dest)
    sass_vars = {
        'front_color': config.front_color,
        'back_color': config.back_color,
        'danger_color': config.danger_color
    }
    compile_sass(src_scss, dest_css, sass_vars)

    # convet icons
    src_icons = '{}/asset'.format(src)
    dest_icons = '{}/asset'.format(dest)
    compile_icon(src_icons, dest_icons, config)
