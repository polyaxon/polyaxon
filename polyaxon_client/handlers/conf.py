import logging

from polyaxon_client import settings

EXCLUDE_DEFAULT_LOGGERS = (
    'polyaxon.client',
    'polyaxon.cli',
)


def setup_logging(handler, exclude=EXCLUDE_DEFAULT_LOGGERS):
    if settings.IN_CLUSTER:
        return

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if handler.__class__ in map(type, logger.handlers):
        del handler

    logger.addHandler(handler)

    for logger_name in exclude:
        logger = logging.getLogger(logger_name)
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())
