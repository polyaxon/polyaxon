from polyaxon.utils import config

ANALYTICS_BACKEND_NOOP = 'noop'
ANALYTICS_BACKEND_PUBLISHER = 'publisher'
ANALYTICS_BACKEND = config.get_string(
    'POLYAXON_ANALYTICS_BACKEND',
    is_optional=True,
    default=ANALYTICS_BACKEND_NOOP,
    options=(ANALYTICS_BACKEND_NOOP, ANALYTICS_BACKEND_PUBLISHER))
