'''
SPEC    : Contains utility functions

EXPORT  : real_theme_name(), short_theme_name()
'''

def real_theme_name(short_name):
    return 'venom-{}'.format(short_name)


def short_theme_name(name):
    return name[len('venom-'):]
