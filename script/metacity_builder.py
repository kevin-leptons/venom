import os
import shutil
import dirsync


from .icon_builder import compile_icon

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

    # create metacity-theme file
    src_theme = '{}/metacity-theme-1.xml'.format(src)
    dest_theme = '{}/metacity-theme-1.xml'.format(dest)
    with open(src_theme, 'r') as src_f:
        data = src_f.read().replace('{{front_color}}', config.front_color)
        data = data.replace('{{back_color}}', config.back_color)
        data = data.replace('{{active_color}}', config.front_color)
        data = data.replace('{{border}}', config.front_color)
        data = data.replace('{{border_focus}}', config.front_color)
        with open(dest_theme, 'w') as dest_f:
            dest_f.write(data)
