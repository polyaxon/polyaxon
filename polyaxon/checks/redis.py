import redis

from checks.base import Check
from checks.results import Result
from db.redis.containers import RedisJobContainers
from db.redis.ephemeral_tokens import RedisEphemeralTokens
from db.redis.sessions import RedisSessions
from db.redis.tll import RedisTTL
from db.redis.to_stream import RedisToStream


class RedisCheck(Check):

    @staticmethod
    def redis_health(connection):
        try:
            info = connection.info()
            return Result(message='Service is healthy, db size {}'.format(info['used_memory']))
        except redis.exceptions.ConnectionError:
            return Result(severity=Result.ERROR)

    @classmethod
    def check(cls):
        results = {}
        result = cls.redis_health(RedisEphemeralTokens.connection())
        if result.is_error():
            results['REDIS_EPH_TOKENS'] = result

        result = cls.redis_health(RedisSessions.connection())
        if result.is_error():
            results['REDIS_SESSIONS'] = result

        result = cls.redis_health(RedisTTL.connection())
        if result.is_error():
            results['REDIS_TTL'] = result

        result = cls.redis_health(RedisToStream.connection())
        if result.is_error():
            results['REDIS_TO_STREAM'] = result

        result = cls.redis_health(RedisJobContainers.connection())
        if result.is_error():
            results['REDIS_CONTAINERS'] = result

        if not results:
            results = {'REDIS': Result()}

        return results
