from subprocess import Popen

from .logger import stdlog, stat_done, stat_err


def install_theme(name):
    '''
    Install theme to /usr/share/themes/<name>
    Install icons to /usr/share/icons/<name>

    :param str name: Name of theme
    :return: 0 on success, -1 on error
    :rtype: int
    '''

    dest = 'dest/{}'.format(name)
    dest_theme = '{}/*'.format(dest)
    dest_icon = '{}/icons/*'.format(dest)
    target_theme = '/usr/share/themes/{}'.format(name)
    target_icon = '/usr/share/icons/{}'.format(name)

    # install theme
    if Popen(['sudo', 'mkdir', '-vp', target_theme]).wait() != 0:
        stdlog(stat_err, 'create theme dir', name)
        return -1
    cmd_theme = [
        'bash', '-c',  'sudo cp -r {} {}'.format(dest_theme, target_theme)
    ]
    if Popen(cmd_theme).wait() != 0:
        stdlog(stat_err, 'copy theme', name)
        return -1

    # install icons
    if Popen(['sudo', 'mkdir', '-vp', target_icon]).wait() != 0:
        stdlog(stat_err, 'create icons dir', name)
        return -1
    cmd_icon = [
        'bash', '-c', 'sudo cp -r {} {}'.format(dest_icon, target_icon)
    ]
    if Popen(cmd_icon).wait() != 0:
        stdlog(stat_err, 'copy icons', name)
        return -1

    return 0


def remove_theme(name):
    '''
    Remove theme to /usr/share/themes/<name>
    Remove icons to /usr/share/icons/<name>

    :param str name: Name of theme
    '''

    target_theme = '/usr/share/themes/{}'.format(name)
    target_icon = '/usr/share/icons/{}'.format(name)

    if Popen(['sudo', 'rm', '-r', target_theme]).wait() != 0:
        stdlog(stat_err, 'can not remove theme', name)
    if Popen(['sudo', 'rm', '-r', target_icon]).wait() != 0:
        stdlog(stat_err, 'can not remove icons', name)

    stdlog(stat_done, 'removed', name)
