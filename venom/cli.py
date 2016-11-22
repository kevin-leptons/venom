import click

from active_theme import active_theme


@click.group()
def cli():
    pass


@cli.command(help='Active theme')
@click.argument('name')
def active(name):
    active_theme(name)
