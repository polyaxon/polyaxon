import redis

from api.utils import config


class RedisPools(object):
    EXPERIMENTS_STATUS = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_EXPERIMENTS_STATUS_URL'))
    JOBS_STATUS = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_JOBS_STATUS_URL'))
    JOB_CONTAINERS = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_JOB_CONTAINERS_URL'))
