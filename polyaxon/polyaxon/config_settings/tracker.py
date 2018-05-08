from polyaxon.utils import config

TRACKER_BACKEND_NOOP = 'noop'
TRACKER_BACKEND_PUBLISHER = 'publisher'
TRACKER_BACKEND = config.get_string(
    'POLYAXON_TRACKER_BACKEND',
    is_optional=True,
    default=TRACKER_BACKEND_NOOP,
    options=(TRACKER_BACKEND_NOOP, TRACKER_BACKEND_PUBLISHER))
