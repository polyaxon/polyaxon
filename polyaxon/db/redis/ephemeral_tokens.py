import base64
import uuid

from typing import Dict, List, Optional

from hestia.crypto import get_hmac

from django.utils.crypto import constant_time_compare

import conf

from db.redis.base import BaseRedisDb
from libs.json_utils import dumps, loads
from polyaxon.settings import RedisPools


class RedisEphemeralTokens(BaseRedisDb):
    """
    RedisEphemeralTokens provides a db to store ephemeral tokens for users jobs
    that requires in cluster authentication to access scoped resources
    """
    KEY_SALT = 'polyaxon.scope.key_salt'
    SEPARATOR = 'XEPH:'

    KEY_EPHEMERAL_TOKENS = 'EPHEMERAL_TOKENS:{}'

    REDIS_POOL = RedisPools.EPHEMERAL_TOKENS

    def __init__(self, key: str = None) -> None:
        self.__dict__['key'] = key or uuid.uuid4().hex
        self.__dict__['_red'] = self._get_redis()

    def __getattr__(self, key: str) -> None:
        state = self.get_state()

        try:
            return state[key] if state else None
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key: str, value: str) -> None:
        state = self.get_state()

        if state is None:
            return

        state[key] = value
        self.set_state(ttl=self.ttl, value=dumps(state))

    def get_state(self) -> Optional[Dict]:
        if not self.redis_key:
            return None

        state_json = self._red.get(self.redis_key)
        if not state_json:
            return None

        return loads(state_json.decode())

    def set_state(self, ttl: int, value: str) -> None:
        self._red.setex(name=self.redis_key, time=ttl, value=value)

    @property
    def redis_key(self) -> str:
        return self.KEY_EPHEMERAL_TOKENS.format(self.key)

    @classmethod
    def generate(cls, scope: str, ttl: int = None) -> 'RedisEphemeralTokens':
        ttl = ttl or conf.get('TTL_EPHEMERAL_TOKEN')
        token = RedisEphemeralTokens()
        salt = uuid.uuid4().hex
        value = dumps({
            'key': token.redis_key,
            'salt': salt,
            'scope': scope,
            'ttl': ttl,
        })
        token.set_state(ttl=ttl, value=value)
        return token

    @classmethod
    def make_token(cls, ephemeral_token: 'RedisEphemeralTokens') -> str:
        """
        Returns a token to be used x number of times to allow a user account to access
        certain resource.
        """
        value = ephemeral_token.key
        if ephemeral_token.scope:
            value += ''.join(ephemeral_token.scope)

        return get_hmac(cls.KEY_SALT + ephemeral_token.salt, value)[::2]

    def clear(self) -> None:
        if not self.redis_key:
            return

        self._red.delete(self.redis_key)

    def check_token(self, token: 'RedisEphemeralTokens') -> bool:
        """
        Check that a token is correct for a given scope token.
        """
        if self.get_state() is None:  # Token expired
            return False

        correct_token = self.make_token(self)
        self.clear()
        return constant_time_compare(correct_token, token)

    @classmethod
    def create_header_token(cls, ephemeral_token: 'RedisEphemeralTokens') -> str:
        token = cls.make_token(ephemeral_token)
        return base64.b64encode(
            '{}{}{}'.format(token,
                            cls.SEPARATOR,
                            ephemeral_token.key).encode('utf-8')).decode("utf-8")

    @classmethod
    def generate_header_token(cls, scope: str) -> str:
        ephemeral_token = RedisEphemeralTokens.generate(scope=scope)
        return cls.create_header_token(ephemeral_token=ephemeral_token)

    @staticmethod
    def get_scope(user: str, model: str, object_id: str) -> List[str]:
        return ['user:{}'.format(user), '{}:{}'.format(model, object_id)]
