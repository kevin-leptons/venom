'''
SPEC    : Provide function to work with colors and image

EXPORT  : rgb_to_gray(), str_to_rgba(), mono_rgba(), vector_mono(),
          bitmap_mono()

AUTHOR  : kevin leptons <kevin.leptons@gmail.com>
'''


import re
import cv2
import numpy
import struct


def rgb_to_gray(rgb):
    '''
    Convert RGB to gray

    :param tuple rgb: Tuple with format (R, G, B)
    :return: Gray color in range [0, 255]
    :rtype: int
    '''

    return int((rgb[0] + rgb[1] + rgb[2]) / 3)


def str_to_rgba(color_str, alpha=1):
    '''
    Convert hex color and alpha to tuple contains RGBA value

    :param str color_str: Color hex string in format #RGB,
        #RRGGBB or color name: red, green, blue, black, white
    :param int alpla: Alpha value in range [0, 255]
    :return: Tuple follow format (R, G, B, A)
    :raise TypeError: On color string can not formatted
    :rtype: tuple
    '''

    if color_str[0] == '#':
        new_str = None
        if len(color_str) == 7:
            # color in RRGGBB format
            new_str = color_str[1:]
        elif len(color_str) == 4:
            # color in RGB format
            new_str = '{}{}{}{}{}{}'.format(
                color_str[1], color_str[1],
                color_str[2], color_str[2],
                color_str[3], color_str[3]
            )
        else:
            raise TypeError('Color format \'{}\' is invalid', color_str)

        rgb = struct.unpack('BBB', new_str.decode('hex'))
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
    Convert color to monochrome mode (front_color, back_color). Color will be
    convert to gray. If gray less than fuzz, return front_color,
    else return back_color

    :param str color: Color string in format #RGB, #RRGGBB or name of color:
        red, green, blue, black, white
    :param str front_color: Color string in format #RGB,
        #RRGGBB or name of color: red, green, blue, black, white
    :param str back_color: Color string in format #RGB,
        #RRGGBB or name of color: red, green, blue, black, white
    :param int fuzz: Value decide converting
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
    '''
    Convert vector image specify by src to monochrome. Then store result
    in dest. If dest is not exist, auto create it

    :param str src: Path to source vector image
    :param str dest: Path to destination vector image
    :param str fcolor: Color string in format #RGB, #RRGGBB or name of color:
        red, green, blue, black, white
    :param str bcolor: Color string in format #RGB, #RRGGBB or name of color:
        red, green, blue, black, white
    :param int fuzz: Valude decide converting
    '''

    with open(src, 'r') as sf:
        try:
            data = sf.read()

            # find all of hex colors in format RGB and RRGGBB
            src_colors = re.findall('[:"]#[a-fA-F0-9]+[;"]', data)

            # remove repeated colors
            src_colors = list(set(src_colors))

            # ignore invalid color format
            for src_color in src_colors[:]:
                if len(src_color) not in (6, 9):
                    src_colors.remove(src_color)

            # create maps for match string and color
            map_colors = [(i, i[1:-1]) for i in src_colors[:]]

            # replace each colors
            for match_str, src_color in map_colors:
                dest_rgba = mono_rgba(src_color, fcolor, bcolor, fuzz)
                dest_str = match_str.replace(src_color, dest_rgba[0])
                data = re.sub(match_str, dest_str, data)

            # create new vector file
            with open(dest, 'w') as df:
                df.write(data)
        except Exception as e:
            raise RuntimeError('Convert file error: {}'.format(src), e)


def bitmap_mono(src, dest, color):
    '''
    Convert bitmap image specify src to monochrome, then store result in
    dest. If dest is not exist, auto create it

    :param str src: Path to source image
    :param str dest: Path to destination image
    :param str color: Color string in format #RGB, #RRGGBB or name of color:
        red, green, blue, black, white
    '''

    src_img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    w = src_img.shape[0]
    h = src_img.shape[1]

    # create new image maxtrix in RGBA
    dest_img = numpy.ndarray(shape=(w, h, 4), dtype=numpy.uint8)

    # convert image grayscale to destination color
    for x in range(w):
        for y in range(h):
            b = src_img.item(x, y, 0)
            g = src_img.item(x, y, 1)
            r = src_img.item(x, y, 2)
            a = src_img.item(x, y, 3)
            gray = rgb_to_gray((r, b, g))

            if a == 0 or gray > 127:
                dest_img.itemset(x, y, 3, 0)
            else:
                dest_img.itemset(x, y, 0, color[2])  # blue
                dest_img.itemset(x, y, 1, color[1])  # green
                dest_img.itemset(x, y, 2, color[0])  # red
                dest_img.itemset(x, y, 3, color[3])  # alpha

    cv2.imwrite(dest, dest_img)
