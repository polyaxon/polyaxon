import redis

from api.utils import config


class RedisPools(object):
    EXPERIMENTS_STATUS = redis.ConnectionPool.from_url(
        config.get_string("REDIS_EXPERIMENTS_STATUS_URL"))
    JOBS_STATUS = redis.ConnectionPool.from_url(
        config.get_string("REDIS_JOBS_STATUS_URL"))
