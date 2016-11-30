import os
import gzip

from os import path, listdir
from os.path import isfile, isdir

from datetime import datetime

from .logger import stdlog, stat_done
from .version import get_version


def compile_manpage(src, dest):
    version = get_version()['version']
    build_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not isdir(dest):
        os.makedirs(dest)

    man_files = [f for f in listdir(src) if isfile(path.join(src, f))]
    for file_name in man_files:
        # read source file and replace correct build date and version
        # then write man page in destination
        src_file = path.join(src, file_name)
        dest_file = path.join(dest, path.splitext(file_name)[0]) + '.gz'
        with open(src_file, 'r') as src_f:
            data = src_f.read().replace('{{build_date}}', build_date)
            data = data.replace('{{version}}', version)

            with gzip.open(dest_file, 'w') as dest_f:
                dest_f.write(data)
            stdlog(stat_done, 'compiled', src_file)
