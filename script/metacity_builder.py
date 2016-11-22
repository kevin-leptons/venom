import os
import shutil
import dirsync


def compile_metacity(src, dest, config):
    '''
    Compile Metatcity theme

    :param str src: Source directory of gnome-shell
    :param str dest: Destination directory
    :param ThemeConfig config: Theme configurations
    '''

    # create destination directory
    if not os.path.isdir(dest):
        os.makedirs(dest)

    # copy metacity-theme file
    src_theme = '{}/metacity-theme-1.xml'.format(src)
    dest_theme = '{}/metacity-theme-1.xml'.format(dest)
    shutil.copyfile(src_theme, dest_theme)

    # copy static files
    src_static = '{}/asset'.format(src)
    dest_static = '{}/asset'.format(dest)
    dirsync.sync(src_static, dest_static, 'sync', create=True)
