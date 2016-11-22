from collections import OrderedDict

from script import ThemeConfig


themes = OrderedDict([
    ('venom-green', ThemeConfig('venom-green', '#55af66', 'black', 'red')),
    ('venom-teal', ThemeConfig('venom-teal', '#008080', 'black', 'red')),
    ('venom-orange', ThemeConfig('venom-orange', '#ff8c00', 'black', 'red'))
])

src = 'src'
dest = 'dest'
