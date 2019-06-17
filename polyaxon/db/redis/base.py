from typing import Any

import redis


class BaseRedisDb(object):
    REDIS_POOL = None

    @classmethod
    def _get_redis(cls) -> Any:
        return redis.Redis(connection_pool=cls.REDIS_POOL,
                           retry_on_timeout=True,
                           socket_keepalive=True)

    @classmethod
    def connection(cls) -> Any:
        return cls._get_redis()
