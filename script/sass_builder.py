'''
SPEC    : Use to compile sass to css

EXPORT  : compile_sass()

AUTHOR  : kevin leptons <kevin.leptons@gmail.com>
'''

import os
import sass


def compile_sass(src, dest, vars={}):
    '''
    Compile sass file to css with pre-defined variables specify by vars

    :param str src: Path to scss source file
    :param str dest: Path to css destination file
    :params dict vars: Optional variables
    '''

    # create string, contains scss variables
    vars_scss = ''
    for key in vars:
        vars_scss += '${}: {};'.format(key, vars[key])

    # read scss soure file
    with open(src, 'r') as f:
        data = f.read()

    # join optional variables to scss data
    scss = vars_scss + data

    # compile scss to css
    css = sass.compile(
        include_paths=[os.path.dirname(src)],
        string=scss
    )

    # create directory contains destination css file
    dest_dir = os.path.dirname(dest)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    # write css result
    with open(dest, 'w') as f:
        f.write(css)
