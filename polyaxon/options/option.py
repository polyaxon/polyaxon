from typing import Optional, Tuple

from options.exceptions import OptionException

NAMESPACE_DB_MARKER = ':'
NAMESPACE_ENV_MARKER = '__'


class OptionStores(object):
    ENV = 'env'
    DB = 'db'
    SETTINGS = 'settings'

    VALUES = {ENV, DB, SETTINGS}


class Option(object):
    key = None
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = None
    typing = None
    default = None
    options = None
    description = None

    @classmethod
    def get_marker(cls) -> str:
        if cls.store == OptionStores.DB:
            return NAMESPACE_DB_MARKER
        else:
            return NAMESPACE_ENV_MARKER

    @classmethod
    def parse_key(cls) -> Tuple[Optional[str], str]:
        marker = cls.get_marker()
        parts = cls.key.split(marker)
        if len(parts) > 2:
            raise OptionException('Option declared with multi-namespace key `{}`.'.format(cls.key))
        if len(parts) == 1:
            return None, cls.key
        return parts[0], marker.join(parts[1:])

    @classmethod
    def get_namespace(cls) -> Optional[str]:
        return cls.parse_key()[0]

    @classmethod
    def get_key_subject(cls):
        return cls.parse_key()[1]
