import redis

from api.utils import config


class RedisPools(object):
    JOB_STATUS = redis.ConnectionPool.from_url(config.get_string("REDIS_CELERY_JOB_STATUS_URL"))
