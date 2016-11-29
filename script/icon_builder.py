import os
import shutil
import imghdr

from .logger import stdlog, stat_done
from .imgproc import str_to_rgba, vector_mono, bitmap_mono


def compile_icon(src, dest, config, fuzz=127):
    color = str_to_rgba(config.front_color, 255)

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
                if os.path.isfile(dest_img) or os.path.islink(dest_img):
                    stdlog(stat_done, 'skiped', file)
                else:
                    os.symlink(os.readlink(src_img), dest_img)
                continue

            # file is exist, skip
            if os.path.isfile(dest_img):
                stdlog(stat_done, 'skiped', file)
                continue

            # file is vector, convert here
            if os.path.splitext(src_img)[1] == '.svg':
                vector_mono(
                    src_img, dest_img,
                    config.front_color, config.back_color, fuzz
                )
            else:
                # file is not image, copy it
                if imghdr.what(src_img) is None:
                    shutil.copyfile(src_img, dest_img)
                    continue

                # file is not vector, convert by here
                bitmap_mono(src_img, dest_img, color)

            stdlog(stat_done, 'converted', file)
