'''
SPEC    : Use write log message in only format

EXPORT  : stat_done, stat_warn, stat_err, stdlog()
'''

stat_done = 'done'
stat_warn = 'warn'
stat_err = 'error'


def stdlog(stat, action, msg):
    '''
    Write log message to stdout

    :param str stat: State of message. It can be successfully, warning or
        error. Use stat_done, stat_warn, stat_err for uniform
    :param str action: Action which perform log
    :param str msg: Message from action
    '''

    print('{} {}: {}'.format(stat, action, msg))
