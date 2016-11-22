from .sass_builder import compile_sass


def compile_gtk(src, dest, config):
    '''
    Compile GTK theme

    :param str src: Source directory of gtk
    :param str dest: Destination directory
    :param ThemeConfig config: Theme configurations
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
