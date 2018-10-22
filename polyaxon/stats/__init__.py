from django.conf import settings

from hestia.service_interface import LazyServiceWrapper

from stats.base import BaseStatsBackend


def get_stats_backend():
    if settings.STATS_BACKEND == settings.STATS_BACKEND_NOOP:
        return 'stats.noop.NoOpStatsBackend'
    if settings.STATS_BACKEND == settings.STATS_BACKEND_DATADOG:
        return 'stats.datadog.DatadogStatsBackend'
    if settings.STATS_BACKEND == settings.STATS_BACKEND_STATSD:
        return 'stats.statsd.StatsdStatsBackend'
    return ''


backend = LazyServiceWrapper(
    backend_base=BaseStatsBackend,
    backend_path=get_stats_backend(),
    options={}
)
backend.expose(locals())
