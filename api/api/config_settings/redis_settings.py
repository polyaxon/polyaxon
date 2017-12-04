import redis

from api.utils import config


class RedisPools(object):
    EXPERIMENTS_STATUS = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_EXPERIMENTS_STATUS_URL'))
    JOBS_STATUS = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_JOBS_STATUS_URL'))
    JOB_CONTAINERS = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_JOB_CONTAINERS_URL'))
    TO_STREAM = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_TO_STREAM_URL'))

redis.Redis(connection_pool=RedisPools.EXPERIMENTS_STATUS).flushall()
redis.Redis(connection_pool=RedisPools.JOBS_STATUS).flushall()
redis.Redis(connection_pool=RedisPools.JOB_CONTAINERS).flushall()
redis.Redis(connection_pool=RedisPools.TO_STREAM).flushall()
