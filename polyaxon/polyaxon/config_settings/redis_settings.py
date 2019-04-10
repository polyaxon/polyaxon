import redis

from polyaxon.config_manager import config


class RedisPools(object):
    JOB_CONTAINERS = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_JOB_CONTAINERS_URL'))
    TO_STREAM = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_TO_STREAM_URL'))
    SESSIONS = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_SESSIONS_URL'))
    EPHEMERAL_TOKENS = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_EPHEMERAL_TOKENS_URL'))
    TTL = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_TTL_URL'))
    HEARTBEAT = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_HEARTBEAT_URL'))
    GROUP_CHECKS = redis.ConnectionPool.from_url(
        config.get_string('POLYAXON_REDIS_GROUP_CHECKS_URL'))
