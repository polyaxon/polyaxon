import pytest

from libs.redis_db import RedisEphemeralTokens
from tests.utils import BaseTest


@pytest.mark.redis_mark
class TestRedisEphemeralTokens(BaseTest):
    def test_objects(self):
        token = RedisEphemeralTokens()
        assert token.key is not None
        assert token.redis_key == RedisEphemeralTokens.KEY_EPHEMERAL_TOKENS.format(token.key)

        assert token.get_state() is None
        assert token.salt is None
        assert token.ttl is None
        assert token.scope is None

        token = RedisEphemeralTokens.generate(scope=token.get_scope(1, 'experiment', 1))

        assert token.get_state() is not None
        assert token.salt is not None
        assert token.ttl == RedisEphemeralTokens.EXPIRATION_TTL
        assert token.scope == token.get_scope(1, 'experiment', 1)
        assert token.check_token('foo') is False
        # Checking delete the token
        assert token.get_state() is None

        token = RedisEphemeralTokens.generate(scope=token.get_scope(1, 'experiment', 1))
        assert token.check_token(None) is False
        # Checking delete the token
        assert token.get_state() is None

        token = RedisEphemeralTokens.generate(scope=token.get_scope(1, 'experiment', 1))
        valid = RedisEphemeralTokens.make_token(token)
        assert token.check_token(valid) is True

        # Checking delete the token
        assert token.get_state() is None
        assert token.salt is None
        assert token.ttl is None
        assert token.scope is None
