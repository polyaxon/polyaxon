# pylint:disable=import-error
from datadog import initialize, ThreadStats
from datadog.util.hostname import get_hostname

from django.utils.functional import cached_property

from stats.base import BaseStatsBackend


class DatadogStatsBackend(BaseStatsBackend):
    def __init__(self, prefix=None, host=None, tags=None, **kwargs):
        self.tags = tags
        self.host = host or get_hostname()
        initialize(**kwargs)
        super().__init__(prefix=prefix)

    def __del__(self):
        try:
            self.stats.stop()
        except TypeError:
            # TypeError: 'NoneType' object is not callable
            pass

    @cached_property
    def stats(self):
        instance = ThreadStats()
        instance.start()
        return instance

    def _incr(self, key, amount=1, sample_rate=1, **kwargs):
        tags = kwargs.get('tags', [])
        if self.tags:
            tags += self.tags
        self.stats.increment(key, amount, sample_rate=sample_rate, tags=tags, host=self.host)
