from typing import Dict


class Result(object):
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    SEVERITY_VALUES = {INFO, WARNING, ERROR}

    def __init__(self, message='Service is healthy', severity=INFO) -> None:
        self.message = message
        if severity not in self.SEVERITY_VALUES:
            raise ValueError('Health check Error not recognized `{}`'.format(severity))
        self.severity = severity

    def __str__(self) -> str:
        return self.message

    @property
    def is_healthy(self) -> bool:
        return self.severity == self.INFO

    @property
    def is_warning(self) -> bool:
        return self.severity == self.WARNING

    @property
    def is_error(self) -> bool:
        return self.severity == self.ERROR

    def to_dict(self) -> Dict:
        return {
            'is_healthy': self.is_healthy,
            'message': self.message,
            'severity': self.severity,
        }
