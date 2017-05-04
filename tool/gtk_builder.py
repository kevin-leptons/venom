'''
SYNOPSIS

    build_gtk_theme(pkg_spec, theme_spec)

DESCRIPTION

    Build GTK theme.

AUTHORS

    Kevin Leptons <kevin.leptons@gmail.com>
'''

from os import path

from .sass_builder import build_sass
from .icon_converter import convert_icon


def build_gtk_theme(pkg_spec, theme_spec):
    src_dir = path.join(pkg_spec.src, 'gtk-3.0')
    dest_dir = path.join(pkg_spec.dest, 'themes', theme_spec.name, 'gtk-3.0')

    # build scss to css
    src_scss = path.join(src_dir, 'gtk.scss')
    dest_css = path.join(dest_dir, 'gtk.css')
    sass_vars = {
        'front_color': theme_spec.front_color,
        'back_color': theme_spec.back_color,
        'danger_color': theme_spec.danger_color
    }
    build_sass(src_scss, dest_css, sass_vars)

    # build mono color asset
    icon_src = path.join(src_dir, 'asset')
    icon_dest = path.join(dest_dir, 'asset')
    convert_icon(icon_src, icon_dest, theme_spec.front_color,
                 theme_spec.back_color)
