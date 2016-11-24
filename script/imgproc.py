import re
import cv2
import numpy
import struct


def rgb_to_gray(rgb):
    # return int(0.21 * rgb[0] + 0.72 * rgb[1] + 0.07 * rgb[2])
    return int((rgb[0] + rgb[1] + rgb[2]) / 3)


def str_to_rgba(color_str, alpha=1):
    '''
    :param str hex_str: Color hex string in format RGB or name of color
        red, green, blue, black, white
    :param int alpla: Alpha value in range [0, 255]
    :return: Tuple follow format (R, G, B, A)
    :raise TypeError: On color string can not formatted
    :rtype: tuple
    '''

    if color_str[0] == '#':
        rgb = struct.unpack('BBB', color_str[1:].decode('hex'))
        return rgb + (alpha,)

    if color_str == 'red':
        return (255, 0, 0, alpha)
    elif color_str == 'green':
        return (0, 255, 0, alpha)
    elif color_str == 'blue':
        return (0, 0, 255, alpha)
    elif color_str == 'black':
        return (0, 0, 0, alpha)
    elif color_str == 'white':
        return (255, 255, 255, alpha)
    else:
        raise TypeError('Color \'{}\' is not supported'.format(color_str))


def mono_rgba(color, front_color, back_color, fuzz):
    '''
    Convert color to color in mono mode (front_color, back_color)

    :return: Tuple with (rgb, alpha)
    :rtype: tuple
    '''

    src_rgb = str_to_rgba(color)
    gray = rgb_to_gray(src_rgb)

    if gray < fuzz:
        return (front_color, 1)
    else:
        return (back_color, 0)


def vector_mono(src, dest, fcolor, bcolor, fuzz=127):

    with open(src, 'r') as sf:
        data = sf.read()

        # find all of hex colors
        src_colors = re.findall('#[a-fA-F0-9]{6}', data)

        # remove repeated colors
        src_colors = set(src_colors)

        # replace each colors
        for src_color in src_colors:
            dest_rgba = mono_rgba(src_color, fcolor, bcolor, fuzz)
            data = re.sub(src_color, dest_rgba[0], data)

        # create new vector file
        with open(dest, 'w') as df:
            df.write(data)
    pass


def bitmap_mono(src, dest, color):
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
