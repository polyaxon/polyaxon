import redis

from api.utils import config


class RedisPools(object):
    JOBS_STATUS = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_JOBS_STATUS_URL'))
    JOB_CONTAINERS = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_JOB_CONTAINERS_URL'))
    TO_STREAM = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_TO_STREAM_URL'))
