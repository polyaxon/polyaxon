import logging
import sys
import traceback

from polyaxon_client import settings
from polyaxon_schemas.utils import local_now


class PolyaxonHandler(logging.Handler):
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S %Z"

    def __init__(self, send_logs, **kwargs):
        self._send_logs = send_logs
        logging.Handler.__init__(self, level=kwargs.get('level', logging.NOTSET))

    def can_record(self, record):
        return not (
            record.name == 'polyaxon.client' or
            record.name == 'polyaxon.cli' or
            record.name.startswith('polyaxon')
        )

    def format_record(self, record):
        return '{} -- {} {}'.format(local_now().strftime(self.DATETIME_FORMAT),
                                    record.levelname,
                                    record.msg)

    def emit(self, record):  # pylint:disable=inconsistent-return-statements
        if settings.IN_CLUSTER or not self.can_record(record):
            return
        try:
            return self._send_logs(self.format_record(record))
        except Exception:
            print("Polyaxon failed creating log record", file=sys.stderr)
            print('{}'.format(record.msg), file=sys.stderr)
            print('{}'.format(traceback.format_exc()), file=sys.stderr)
