'''
SYNOPSIS

    convert_icon(src, dest, front_color, back_color, skips=[], fuzz=127)

DESCRIPTION

    Recursive convert icons in src directory to monochrome, then store
    resutl in dest directory with same structure. It not change contents
    and size of image. It supported two type of image: bitmap and vector.
    With bitmap, supported RGBA chanels. With vector, not really read
    specifications of svg, simple is find and replace hex color.

AUTHORS

    Kevin Leptons <kevin.leptons@gmail.com>
'''

import os
import imghdr
from os import path, symlink, readlink
from os.path import isfile, islink

from .logger import stdlog, stat_done
from .imgproc import str_to_rgba, vector_mono, bitmap_mono
from .shell import cp, mkdir


def convert_icon(src, dest, front_color, back_color, skips=[], fuzz=127):
    color = str_to_rgba(front_color, 255)

    for root, dirs, files in os.walk(src):
        rpath = root[len(src):]
        if len(rpath) > 0:
            if rpath[0] == '/':
                rpath = rpath[1:]
        dest_dir = path.join(dest, rpath)
        mkdir(dest_dir)

        # convert for each image files
        for file in files:
            src_img = path.join(root, file)
            dest_img = path.join(dest_dir, file)

            # file is symbol link, copy it
            if islink(src_img):
                if isfile(dest_img) or islink(dest_img):
                    stdlog(stat_done, 'skiped', file)
                else:
                    symlink(readlink(src_img), dest_img)
                continue

            # file is exist, skip
            if isfile(dest_img):
                stdlog(stat_done, 'skiped', file)
                continue

            # file is vector, convert here
            if path.splitext(src_img)[1] == '.svg':
                vector_mono(
                    src_img, dest_img,
                    front_color, back_color, fuzz
                )
            else:
                # file is not image, copy it
                if imghdr.what(src_img) is None:
                    cp(src_img, dest_img)
                    continue

                # file is not vector, convert by here
                bitmap_mono(src_img, dest_img, color)

            stdlog(stat_done, 'converted', file)
