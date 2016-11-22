class ThemeNotFoundError(Exception):
    def __init__(self, name):
        self.error = 'Not found theme {}'.format(name)

    def __str__(self):
        return self.error
