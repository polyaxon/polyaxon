from typing import Optional

import conf

from db.redis.base import BaseRedisDb
from options.registry.ttl import TTL_KEEP_STATUSES
from polyaxon.settings import RedisPools


class RedisStatuses(BaseRedisDb):
    """
    RedisStatuses provides a db to store and get fast access to data related to statuses.
    """
    KEY_STATUSES = 'STATUSES:{}'

    REDIS_POOL = RedisPools.STATUSES

    @classmethod
    def get_status_key(cls, job: str) -> str:
        return cls.KEY_STATUSES.format(job)

    @classmethod
    def set_status(cls, job: str, status: str, ttl: int = None) -> None:
        ttl = ttl or conf.get(TTL_KEEP_STATUSES)
        status_key = cls.get_status_key(job=job)
        red = cls._get_redis()
        red.setex(name=status_key, time=ttl, value=status)

    @classmethod
    def get_status(cls, job: str) -> Optional[str]:
        status_key = cls.get_status_key(job=job)
        red = cls._get_redis()
        status = red.get(status_key)
        if not status:
            return None
        return status.decode('utf-8')

    @classmethod
    def delete_status(cls, job: str) -> None:
        status_key = cls.get_status_key(job=job)
        red = cls._get_redis()
        red.delete(status_key)
