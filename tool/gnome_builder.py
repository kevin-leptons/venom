'''
SYNOPSIS

    build_gnome_theme(pkg_spec, theme_spec)

DESCRIPTION

    Build gnome-shell theme from. All of asset store in src directory,
    compiler will read, build by config. Then store result in dest directory

AUTHORS

    Kevin Leptons <kevin.leptons@gmail.com>
'''

from os import path

from .sass_builder import build_sass
from .icon_converter import convert_icon


def build_gnome_theme(pkg_spec, theme_spec):
    src_dir = path.join(pkg_spec.src, 'gnome-shell')
    dest_dir = path.join(pkg_spec.dest, 'themes', theme_spec.name,
                         'gnome-shell')

    # build sass to css
    scss_src = path.join(src_dir, 'gnome-shell.scss')
    css_dest = path.join(dest_dir, 'gnome-shell.css')
    sass_vars = {
        'front_color': theme_spec.front_color,
        'back_color': theme_spec.back_color,
        'danger_color': theme_spec.danger_color
    }
    build_sass(scss_src, css_dest, sass_vars)

    # build mono color icons
    icon_src = path.join(src_dir, 'asset')
    icon_dest = path.join(dest_dir, 'asset')
    convert_icon(icon_src, icon_dest, theme_spec.front_color,
                 theme_spec.back_color)
