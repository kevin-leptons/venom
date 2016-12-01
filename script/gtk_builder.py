'''
SPEC    : Use to build GTK3 theme

EXPORT  : compile_gtk()

AUTHOR  : kevin leptons <kevin.leptons@gmail.com>
'''

from .sass_builder import compile_sass


def compile_gtk(src, dest, config):
    '''
    Compile GTK3 theme. Compile will asset in src directory, build by config
    then store result in dest directory

    :param str src: Directory contains asset of GTK3 theme
    :param str dest: Directory to store result
    :param ThemeConfig config: Theme configuration
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
