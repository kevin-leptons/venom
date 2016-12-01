'''
SPEC    : Specify theme configuration

EXPORT  : ThemeConfig()

AUTHOR  : kevin leptons <kevin.leptons@gmail.com>
'''

class ThemeConfig(object):
    '''
    Configuration of theme. Use by compiler

    :param str name: Name of theme
    :param str front_color: Color use for text, border
    :param str back_color: Color use for background
    :param str danger_color: Color use for critical action
    '''

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
