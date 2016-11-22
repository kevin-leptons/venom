stat_done = 'done'
stat_warn = 'warn'
stat_err = 'error'


def stdlog(stat, action, msg):
    print '{} {}: {}'.format(stat, action, msg)
