from polyaxon.settings import redis

class BaseRedisDb(object):
    REDIS_POOL = None

    @classmethod
    def _get_redis(cls):
        return redis.Redis(connection_pool=cls.REDIS_POOL)
