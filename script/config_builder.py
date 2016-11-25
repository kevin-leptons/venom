import os
import ConfigParser


def compile_config(src, dest, config):
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
