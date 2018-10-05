class Result(object):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    SEVERITY_VALUES = {INFO, WARNING, ERROR}

    def __init__(self, message='Service is healthy', severity=INFO):
        self.message = message
        if severity not in self.SEVERITY_VALUES:
            raise ValueError('Health check Error not recognized `{}`'.format(severity))
        self.severity = severity

    def __str__(self):
        return self.message

    @property
    def is_healthy(self):
        return self.severity == self.INFO

    @property
    def is_error(self):
        return not self.is_healthy

    @property
    def is_warning(self):
        return self.severity == self.WARNING

    @property
    def is_error(self):
        return self.severity == self.ERROR
