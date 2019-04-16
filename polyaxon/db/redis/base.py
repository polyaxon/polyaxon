from typing import Any

import redis


class BaseRedisDb(object):
    REDIS_POOL = None

    @classmethod
    def _get_redis(cls) -> Any:
        return redis.StrictRedis(connection_pool=cls.REDIS_POOL)

    @classmethod
    def connection(cls) -> Any:
        return cls._get_redis()
