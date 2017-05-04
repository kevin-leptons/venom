'''
SYNOPSIS

    build_icon_theme(pkg_spec, theme_spec)

DESCRIPTION

    Recursive convert icons in src directory to monochrome, then store
    resutl in dest directory with same structure. It not change contents
    and size of image. It supported two type of image: bitmap and vector.
    With bitmap, supported RGBA chanels. With vector, not really read
    specifications of svg, simple is find and replace hex color

AUTHORS

    Kevin Leptons <kevin.leptons@gmail.com>
'''

from os import path

from .icon_converter import convert_icon


def build_icon_theme(pkg_spec, theme_spec):
    src = path.join(pkg_spec.src, 'icons')
    dest = path.join(pkg_spec.dest, 'themes', theme_spec.name, 'icons')
    convert_icon(src, dest, theme_spec.front_color, theme_spec.back_color)
