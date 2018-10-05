from polyaxon.settings import redis


class BaseRedisDb(object):
    REDIS_POOL = None

    @classmethod
    def _get_redis(cls):
        return redis.StrictRedis(connection_pool=cls.REDIS_POOL)

    @classmethod
    def connection(cls):
        return cls._get_redis()
