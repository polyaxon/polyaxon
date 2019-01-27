import conf

from db.redis.base import BaseRedisDb
from polyaxon.settings import RedisPools


class GroupChecks(BaseRedisDb):
    """
    GroupChecks provides a db to store group last check to start new experiments.
    """
    KEY_CHECKED = 'group.checked:{}'
    KEY_DELAYED = 'group.delayed:{}'

    # If a group started a task in this interval we schedule at most one afterwards
    REDIS_POOL = RedisPools.GROUP_CHECKS

    def __init__(self, group) -> None:
        self.__dict__['key'] = group
        self.__dict__['_red'] = self._get_redis()

    def __getattr__(self, key: str):
        value = self.get_value()

        try:
            return value
        except KeyError as e:
            raise AttributeError(e)

    @property
    def redis_key_checked(self) -> str:
        return self.KEY_CHECKED.format(self.key)

    @property
    def redis_key_delayed(self) -> str:
        return self.KEY_DELAYED.format(self.key)

    def is_checked(self) -> bool:
        """One task ran (checked)."""
        if not self.redis_key_checked:
            return False

        value = self._red.get(self.redis_key_checked)
        if not value:
            return False

        return True

    def is_delayed(self) -> bool:
        """One task ran (checked), and one task has been delayed."""
        if not self.redis_key_delayed:
            return False

        value = self._red.get(self.redis_key_delayed)
        if not value:
            return False

        return True

    def check(self) -> None:
        self._red.setex(name=self.redis_key_checked,
                        value=1,
                        time=conf.get('GROUP_CHECKS_INTERVAL'))

    def delay(self) -> None:
        self.check()
        self._red.setex(name=self.redis_key_delayed,
                        value=1,
                        time=conf.get('GROUP_CHECKS_INTERVAL'))

    def clear(self) -> None:
        if self.redis_key_checked:
            self._red.delete(self.redis_key_checked)
        if self.redis_key_delayed:
            self._red.delete(self.redis_key_delayed)
