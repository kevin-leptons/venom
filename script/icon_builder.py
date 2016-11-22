import os
import shutil
import imghdr
import cv2
import numpy
import struct

from .logger import stdlog, stat_done


def hex_to_rgba(hex_str, alpha):
    '''
    :param str hex_str: Color hex string in format '#RRGGBB'
    :param int alpla: Alpha value in range [0, 255]
    :return: Tuple follow format (R, G, B, A)
    :rtype: tuple
    '''
    rgb = struct.unpack('BBB', hex_str[1:].decode('hex'))
    return rgb + (alpha,)


def make_imgmono(src, dest, color):
    src_img = cv2.imread(src, cv2.IMREAD_GRAYSCALE)
    w = src_img.shape[0]
    h = src_img.shape[1]

    # create new image maxtrix in RGBA
    dest_img = numpy.ndarray(shape=(w, h, 4), dtype=numpy.uint8)

    # convert image grayscale to destination color
    for x in range(w):
        for y in range(h):
            if src_img.item(x, y) <= 127:
                dest_img.itemset(x, y, 0, color[2]) # blue
                dest_img.itemset(x, y, 1, color[1]) # green
                dest_img.itemset(x, y, 2, color[0]) # red
                dest_img.itemset(x, y, 3, color[3]) # alpha
            else:
                dest_img.itemset(x, y, 3, 0)

    cv2.imwrite(dest, dest_img)

def compile_icon(src, dest, config):
    color = hex_to_rgba(config.front_color, 255)

    for root, dirs, files in os.walk(src):
        path = root[len(src):]
        dest_dir = '{}/{}'.format(dest, path).replace('//', '/').rstrip('/')
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)

        # convert for each file
        for file in files:
            src_img = '{}/{}'.format(root, file)
            dest_img = '{}/{}'.format(dest_dir, file)

            # file is symbol link, copy it
            if os.path.islink(src_img):
                if not os.path.islink(dest_img):
                    os.symlink(os.readlink(src_img), dest_img)
                else:
                    stdlog(stat_done, 'skiped', file)
                continue

            # file is exist, skip
            if os.path.isfile(dest_img):
                stdlog(stat_done, 'skiped', file)
                continue

            # file is not image, copy it
            if imghdr.what(src_img) is None:
                shutil.copyfile(src_img, dest_img)
                continue

            # convert image to mono image
            make_imgmono(src_img, dest_img, color)

            stdlog(stat_done, 'converted', file)
