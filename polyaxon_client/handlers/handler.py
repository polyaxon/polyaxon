import logging

from hestia.logging_utils import LogSpec

from polyaxon_client import settings
from polyaxon_client.logger import logger


class PolyaxonHandler(logging.Handler):

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
        return LogSpec(log_line=record.msg, log_level=record.levelname)

    def emit(self, record):  # pylint:disable=inconsistent-return-statements
        if settings.IN_CLUSTER or not self.can_record(record):
            return
        try:
            return self._send_logs(self.format_record(record))
        except Exception:
            logger.warning("Polyaxon failed creating log record")
