from polyaxon.config_manager import config

STATS_BACKEND_NOOP = 'noop'
STATS_BACKEND_DATADOG = 'datadog'
STATS_BACKEND_STATSD = 'statsd'
STATS_BACKEND = config.get_string(
    'POLYAXON_STATS_BACKEND',
    is_optional=True,
    default=STATS_BACKEND_NOOP,
    options=(STATS_BACKEND_NOOP, STATS_BACKEND_DATADOG, STATS_BACKEND_STATSD))
