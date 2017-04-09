from collections import OrderedDict

from script import ThemeConfig


themes = OrderedDict([
    ('venom-black', ThemeConfig('venom-black', '#000000', '#fefefe', 'red')),
    ('venom-orange', ThemeConfig('venom-orange', '#ff8c00', 'black', 'red')),
    ('venom-green', ThemeConfig('venom-green', '#55af66', 'black', 'red')),
])

src = 'src'
dest = 'dest'
