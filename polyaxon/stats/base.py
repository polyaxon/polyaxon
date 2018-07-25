from django.conf import settings

from random import random
from threading import local


class BaseStatsBackend(local):
    def __init__(self, prefix=None):
        if prefix is None:
            prefix = settings.DEFAULT_STATS_PREFIX
        self.prefix = prefix

    def _get_key(self, key):
        if self.prefix:
            return '{}.{}'.format(self.prefix, key)
        return key

    def _should_sample(self, sample_rate):
        return sample_rate >= 1 or random() >= 1 - sample_rate

    def _incr(self, key, amount=1, sample_rate=1, **kwargs):
        raise NotImplementedError

    def incr(self, key, amount=1, sample_rate=1, **kwargs):
        self._incr(key=self._get_key(key), amount=amount, sample_rate=sample_rate, **kwargs)
