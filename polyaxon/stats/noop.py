from stats.base import BaseStatsBackend


class NoOpStatasBackend(BaseStatsBackend):
    def _incr(self, key, amount=1, sample_rate=1, **kwargs):
        pass
