# pylint:disable=import-error
import statsd

from stats.base import BaseStatsBackend


class StatsdStatsBackend(BaseStatsBackend):
    def __init__(self, prefix=None, host='localhost', port=8125):
        self.client = statsd.StatsClient(host=host, port=port)
        super().__init__(prefix=prefix)

    def _incr(self, key, amount=1, sample_rate=1, **kwargs):
        self.client.incr(key, amount, sample_rate)
