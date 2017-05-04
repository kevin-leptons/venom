'''
SPEC    : Build icon theme

EXPORT  : compile_icon()

AUTHOR  : kevin leptons <kevin.leptons@gmail.com>
'''

import os
import sys
from subprocess import Popen

from .icon_converter import convert_icon
from .logger import stdlog, stat_done


def compile_icon(src, dest, config, pkg_config, fuzz=127):
    '''
    Recursive convert icons in src directory to monochrome, then store
    resutl in dest directory with same structure. It not change contents
    and size of image. It supported two type of image: bitmap and vector.
    With bitmap, supported RGBA chanels. With vector, not really read
    specifications of svg, simple is find and replace hex color

    :param str src: Directory contains icons to convert
    :param str dest: Directory to store result
    :param ThemeConfig config: Theme configuration
    :param PackageConfig pkg_config: Contains configuration of package
    :param int fuzz: Value will decide source color must be convert to what.
        Source color will be convert to gray. If gray less than fuzz, it
        will convert to front_color, else convert to back_color
    '''

    # compile icons
    convert_icon(src, dest, config, ['cursors'], fuzz)

    # compile cursor icons
    _compile_cursor(src, dest, config, pkg_config, fuzz)


def _compile_cursor(src, dest, config, pkg_config, fuzz=127):
    tmp = '{}/tmp/{}'.format(pkg_config.dest, config.name)
    tmp_svg = '{}/cursor-svg'.format(tmp)
    tmp_png_32 = '{}/cursor-png-32'.format(tmp)
    tmp_png_64 = '{}/cursor-png-64'.format(tmp)
    cursor_src = '{}/cursors'.format(src)
    cursor_dest = '{}/cursors'.format(dest)
    cursor_config = '{}/cursor-config'.format(pkg_config.src)

    if not os.path.isdir(tmp_svg):
        os.makedirs(tmp_svg)
    if not os.path.isdir(tmp_png_32):
        os.makedirs(tmp_png_32)
    if not os.path.isdir(tmp_png_64):
        os.makedirs(tmp_png_64)
    if not os.path.isdir(cursor_dest):
        os.makedirs(cursor_dest)

    # convert raw svg files to svg with correct color
    # and copy configuration directory
    convert_icon(cursor_src, tmp_svg, config, [], fuzz)

    # covert svg files to png
    for (root, dirs, files) in os.walk(tmp_svg):
        # skip for child directories
        if len(root) > len(tmp_svg):
            continue
        for svg_file in files:
            input_basename = os.path.basename(svg_file)
            input_name = os.path.splitext(input_basename)[0]
            input_file = '{}/{}'.format(root, svg_file)

            # 32x32 pixels
            output_file_32 = '{}/{}.png'.format(tmp_png_32, input_name)
            if os.path.isfile(output_file_32):
                stdlog(stat_done, 'skiped', output_file_32)
                continue
            cmd = [
                'inkscape', '-z', '-e', output_file_32, '-w', '32', '-h', '32',
                input_file
            ]
            if Popen(cmd).wait() != 0:
                sys.exit(1)

            # 64x64 pixels
            output_file_64 = '{}/{}.png'.format(tmp_png_64, input_name)
            if os.path.isfile(output_file_64):
                stdlog(stat_done, 'skiped', output_file_64)
                continue
            cmd = [
                'inkscape', '-z', '-e', output_file_64, '-w', '64', '-h', '64',
                input_file
            ]
            if Popen(cmd).wait() != 0:
                sys.exit(1)

    # convert png files above to cusor files
    for (root, dirs, files) in os.walk(cursor_config):
        # skip for child directories
        if len(root) > len(cursor_config):
            continue
        for config_file in files:
            input_file = '{}/{}'.format(root, config_file)
            config_basename = os.path.basename(config_file)
            config_name = os.path.splitext(config_basename)[0]
            output_file = '{}/{}'.format(cursor_dest, config_name)
            if os.path.isfile(output_file):
                stdlog(stat_done, 'skiped', output_file)
                continue
            cmd = [
                'xcursorgen', input_file, output_file,
                '-p', tmp
            ]
            if Popen(cmd).wait() != 0:
                sys.exit(1)

    # create symbol links
    f = open('{}/cursor-alias.txt'.format(pkg_config.src), 'r')
    for line in f:
        parts = line.strip().split(' ')
        cmd_ln = ['ln', '-srf', parts[1], parts[0]]
        if Popen(cmd_ln, cwd=cursor_dest).wait() != 0:
            sys.exit(1)
    f.close()
