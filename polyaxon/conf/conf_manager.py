from collections import namedtuple
from typing import Any

from hestia.datetime_typing import AwareDT

from django.utils import timezone

from conf.exceptions import ConfException
from options.option import OptionStores


class CachedOptionSpec(namedtuple("CachedOptionSpec", "value datetime")):
    pass


class ConfCacheManager(object):
    CACHE_INTERVAL = 20
    INVALIDED_OPTION = 'INVALIDED_OPTION'

    def __init__(self):
        self._state = {}

    def clear_namespace(self, namespace: str, store: str) -> None:
        if store not in OptionStores:
            raise ConfException('`{}` is an invalid store.'.format(store))
        marker_namespace = '{}{}'.format(namespace, store)
        for key in self._state:
            if key.startswith[marker_namespace]:
                del self._state[key]

    def clear_key(self, key: str) -> None:
        self._state.pop(key, None)

    def clear(self) -> None:
        self._state = {}

    @classmethod
    def is_valid_value(cls, value: Any):
        return value != cls.INVALIDED_OPTION

    @staticmethod
    def is_valid_cache(value_datetime: AwareDT) -> bool:
        return timezone.now() < value_datetime

    def get_from_cache(self, key: str) -> Any:
        cached_option = self._state.get(key)
        if cached_option and self.is_valid_cache(cached_option.datetime):
            return cached_option.value
        self.clear_key(key=key)
        return self.INVALIDED_OPTION

    def set_to_cache(self, key: str, namespace: str = None) -> None:
        pass


conf_cache_manager = ConfCacheManager()
