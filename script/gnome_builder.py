import dirsync

from .sass_builder import compile_sass


def compile_gnome(src, dest, config):
    '''
    Compile gnome-shell theme

    :param str src: Source directory of gnome-shell
    :param str dest: Destination directory
    :param ThemeConfig config: Theme configurations
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

    # copy static files
    src_static = '{}/asset'.format(src)
    dest_static = '{}/asset'.format(dest)
    dirsync.sync(src_static, dest_static, 'sync', create=True)
