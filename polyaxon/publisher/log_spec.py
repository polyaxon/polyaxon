from django.utils.timezone import now

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"


def log_spec(log_line, name='', timestamp=None, log_level=None):
    return '{timestamp}{log_level}{name} -- {log_line}'.format(
        log_line=log_line,
        name=' {}'.format(name) if name else '',
        timestamp=timestamp or now().strftime(DATETIME_FORMAT),
        log_level=' {}'.format(log_level) if log_level else '')
