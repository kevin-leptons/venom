'''
SPEC    : Use to create configuration file of theme

EXPORT  : compile_config()

AUTHOR  : kevin leptons <kevin.leptons@gmail.com>
'''

import os
import ConfigParser


def compile_config(src, dest, config):
    '''
    Create configuration file of theme from raw file with main section 'THEME'

    :param str src: Not use
    :param strc dest: Path to new configuration file
    :param ThemeConfig config: Configuration of theme
    '''

    section = 'THEME'
    config_parser = ConfigParser.RawConfigParser()
    config_parser.add_section(section)

    config_parser.set(section, 'front_color', config.front_color)
    config_parser.set(section, 'back_color', config.back_color)
    config_parser.set(section, 'danger_color', config.danger_color)

    if not os.path.isdir(dest):
        os.makedirs(dest)

    config_file = '{}/theme.conf'.format(dest)
    with open(config_file, 'wb') as f:
        config_parser.write(f)
