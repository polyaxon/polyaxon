import uuid

from typing import Any, Dict, Optional

from django.http import HttpRequest

from db.redis.base import BaseRedisDb
from libs.json_utils import dumps, loads
from polyaxon.settings import RedisPools


class RedisSessions(BaseRedisDb):
    """
    RedisSessions provides a db to store data related to a request session.
    Useful for storing data too large to be stored into the session cookie.
    The session store will expire if values are not modified within the provided ttl.

    Example:
        >>> store = RedisSessions(request, 'github')
        >>> store.regenerate()
        >>> store.some_value = 'some value'

        The value will be available across requests as long as the same same store
        name is used.

        >>> store.some_value
        'my value'

        The store may be destroyed before it expires using the ``clear`` method.

        >>> store.clear()
    """
    EXPIRATION_TTL = 10 * 60
    KEY_SESSION_CACHE = 'SESSION_CACHE:{}:{}'
    KEY_SESSION_KEYS = 'SESSION_KEYS:{}'

    REDIS_POOL = RedisPools.SESSIONS

    def __init__(self, request: HttpRequest, prefix: str, ttl: int = EXPIRATION_TTL) -> None:
        self.__dict__['request'] = request
        self.__dict__['prefix'] = prefix
        self.__dict__['ttl'] = ttl
        self.__dict__['_red'] = self._get_redis()

    @property
    def session_key(self) -> str:
        return self.KEY_SESSION_KEYS.format(self.prefix)

    @property
    def redis_key(self) -> str:
        return self.request.session.get(self.session_key)

    def regenerate(self, initial_state: Dict = None) -> None:
        if initial_state is None:
            initial_state = {}

        redis_key = self.KEY_SESSION_CACHE.format(self.prefix, uuid.uuid4().hex)

        self.request.session[self.session_key] = redis_key

        value = dumps(initial_state)
        self._red.setex(name=redis_key, time=self.ttl, value=value)

    def clear(self) -> None:
        if not self.redis_key:
            return

        self._red.delete(self.redis_key)
        del self.request.session[self.session_key]

    def is_valid(self) -> bool:
        return self.redis_key and self._red.get(self.redis_key)

    def get_state(self) -> Optional[Dict]:
        if not self.redis_key:
            return None

        state_json = self._red.get(self.redis_key)
        if not state_json:
            return None

        return loads(state_json.decode())

    def __getattr__(self, key: str) -> Optional[Dict]:
        state = self.get_state()

        try:
            return state[key] if state else None
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key: str, value: Any) -> None:
        state = self.get_state()

        if state is None:
            return

        state[key] = value
        self._red.setex(name=self.redis_key, time=self.ttl, value=dumps(state))
