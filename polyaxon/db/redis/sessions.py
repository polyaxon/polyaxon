import uuid

from libs.json_utils import dumps, loads
from polyaxon.settings import RedisPools, redis

from db.redis.base import BaseRedisDb


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

    def __init__(self, request, prefix, ttl=EXPIRATION_TTL):
        self.__dict__['request'] = request
        self.__dict__['prefix'] = prefix
        self.__dict__['ttl'] = ttl
        self.__dict__['_red'] = self._get_redis()

    @property
    def session_key(self):
        return self.KEY_SESSION_KEYS.format(self.prefix)

    @property
    def redis_key(self):
        return self.request.session.get(self.session_key)

    def regenerate(self, initial_state=None):
        if initial_state is None:
            initial_state = {}

        redis_key = self.KEY_SESSION_CACHE.format(self.prefix, uuid.uuid4().hex)

        self.request.session[self.session_key] = redis_key

        value = dumps(initial_state)
        self._red.setex(name=redis_key, time=self.ttl, value=value)

    def clear(self):
        if not self.redis_key:
            return

        self._red.delete(self.redis_key)
        del self.request.session[self.session_key]

    def is_valid(self):
        return self.redis_key and self._red.get(self.redis_key)

    def get_state(self):
        if not self.redis_key:
            return None

        state_json = self._red.get(self.redis_key)
        if not state_json:
            return None

        return loads(state_json.decode())

    def __getattr__(self, key):
        state = self.get_state()

        try:
            return state[key] if state else None
        except KeyError as e:
            raise AttributeError(e)

    def __setattr__(self, key, value):
        state = self.get_state()

        if state is None:
            return

        state[key] = value
        self._red.setex(name=self.redis_key, time=self.ttl, value=dumps(state))

