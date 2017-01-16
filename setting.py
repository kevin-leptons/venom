from collections import OrderedDict

from script import ThemeConfig


themes = OrderedDict([
    ('venom-black', ThemeConfig('venom-black', '#000000', '#fefefe', 'red')),
    ('venom-white', ThemeConfig('venom-white', '#bbbbbb', '#010101', 'red')),
    ('venom-orange', ThemeConfig('venom-orange', '#ff8c00', 'black', 'red')),
    ('venom-green', ThemeConfig('venom-green', '#55af66', 'black', 'red')),
    ('venom-teal', ThemeConfig('venom-teal', '#008080', 'black', 'red')),
    ('venom-coffee', ThemeConfig('venom-coffee', '#854442', '#fff4e6', 'red'))
])

src = 'src'
dest = 'dest'
