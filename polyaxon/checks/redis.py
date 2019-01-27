from typing import Dict

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
    def redis_health(connection) -> Result:
        try:
            info = connection.info()
            return Result(message='Service is healthy, db size {}'.format(info['used_memory']))
        except redis.exceptions.ConnectionError:
            return Result(message='Service unable to connect, "Connection error".',
                          severity=Result.ERROR)
        except Exception as e:
            return Result(message='Service unable to connect, encountered error "{}".'.format(e),
                          severity=Result.ERROR)

    @classmethod
    def run(cls) -> Dict:
        results = {}
        result = cls.redis_health(RedisEphemeralTokens.connection())
        if not result.is_healthy:
            results['REDIS_EPH_TOKENS'] = result

        result = cls.redis_health(RedisSessions.connection())
        if not result.is_healthy:
            results['REDIS_SESSIONS'] = result

        result = cls.redis_health(RedisTTL.connection())
        if not result.is_healthy:
            results['REDIS_TTL'] = result

        result = cls.redis_health(RedisToStream.connection())
        if not result.is_healthy:
            results['REDIS_TO_STREAM'] = result

        result = cls.redis_health(RedisJobContainers.connection())
        if not result.is_healthy:
            results['REDIS_CONTAINERS'] = result

        if not results:
            results = {'REDIS': Result()}

        return results
