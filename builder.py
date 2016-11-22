#!/usr/bin/env python

# DESCRIPTIONS
#
# Build GTK3 theme. Builder will mix color and build theme package.
# It contains
#   - GTK3 theme
#   - GNOME shell theme
#   - Icon theme
#
# USAGE
#
# $ builder build [OPTIONS]
#
# OPTIONS
#
# --name: Name of theme package
# --front-color: Color to display text, border
# --back-color: Color for background
# --danger-color: Color for critical action
#
# Results of building will store in dest/<name>
#
# EXAMPLES
#
# $ builder build --name "green-on-black" \
#                 --front-color "#55af66" --back-color "#000000" \
#                 --danger-color orange

import click

from script import ThemeConfig, compile_theme

@click.group()
def cli():
    pass


@cli.command(help='Build complete theme package')
@click.option('--name', required=True, help='Name of theme')
@click.option('--front-color', required=True, help='Forground color')
@click.option('--back-color', required=True, help='Background color')
@click.option('--danger-color', required=True, help='Danger color')
def build(name, front_color, back_color, danger_color):
    src = 'src'
    dest = 'dest'
    dest_theme = '{}/{}'.format(dest, name)
    config = ThemeConfig(name, front_color, back_color, danger_color)

    compile_theme(src, dest_theme, config)


cli()
