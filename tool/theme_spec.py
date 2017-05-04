'''
SYNOPSIS

    class ThemeSpec

    THEME_SPECS

DESCRIPTION

    Specify them arguments and give list of specs in THEME_SPECS.

AUTHOR

    Kevin Leptons <kevin.leptons@gmail.com>
'''

from collections import OrderedDict


class ThemeSpec(object):
    def __init__(self, name, front_color, back_color, danger_color):
        self._name = name
        self._front_color = front_color
        self._back_color = back_color
        self._danger_color = danger_color

    @property
    def name(self):
        return self._name

    @property
    def front_color(self):
        return self._front_color

    @property
    def back_color(self):
        return self._back_color

    @property
    def danger_color(self):
        return self._danger_color


THEME_SPECS = OrderedDict([
    ('venom-black', ThemeSpec('venom-black', '#000000', '#fefefe', 'red')),
    ('venom-orange', ThemeSpec('venom-orange', '#ff8c00', 'black', 'red')),
    ('venom-green', ThemeSpec('venom-green', '#55af66', 'black', 'red')),
])
