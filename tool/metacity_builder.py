'''
SYNOPSIS

    build_metacity_theme(pkg_spec, theme_spec)

DESCRIPTION

    Read metacity-theme-1 is specify by src, replace few of information then
    write to dest

AUTHORS

    Kevin Leptons <kevin.leptons@gmail.com>
'''

from os import path

from .shell import mkdir


def build_metacity_theme(pkg_spec, theme_spec):
    dest_dir = path.join(pkg_spec.dest, 'themes', theme_spec.name,
                         'metacity-1')
    mkdir(dest_dir)

    src_theme = path.join(pkg_spec.src, 'metacity-1/metacity-theme-1.xml')
    dest_theme = path.join(dest_dir, 'metacity-theme-1.xml')
    f = open(src_theme, 'r')
    data = f.read()
    f.close()
    data = data.replace('{{front_color}}', theme_spec.front_color)
    data = data.replace('{{back_color}}', theme_spec.back_color)
    data = data.replace('{{active_color}}', theme_spec.front_color)
    data = data.replace('{{border}}', theme_spec.front_color)
    data = data.replace('{{border_focus}}', theme_spec.front_color)
    f = open(dest_theme, 'w+')
    f.write(data)
    f.close()
