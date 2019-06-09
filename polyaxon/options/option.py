from typing import Optional, Tuple

from rhea import parser

from options.exceptions import OptionException

NAMESPACE_DB_OPTION_MARKER = ':'
NAMESPACE_DB_CONFIG_MARKER = '__'
NAMESPACE_SETTINGS_MARKER = '__'
NAMESPACE_ENV_MARKER = '__'


class OptionStores(object):
    ENV = 'env'
    DB_OPTION = 'db_option'
    DB_CONFIG = 'db_config'
    SETTINGS = 'settings'

    VALUES = {ENV, DB_OPTION, DB_CONFIG, SETTINGS}


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
        if cls.store == OptionStores.DB_OPTION:
            return NAMESPACE_DB_OPTION_MARKER
        elif cls.store == OptionStores.DB_CONFIG:
            return NAMESPACE_DB_CONFIG_MARKER
        elif cls.store == OptionStores.SETTINGS:
            return NAMESPACE_SETTINGS_MARKER

        return NAMESPACE_ENV_MARKER

    @classmethod
    def parse_key(cls) -> Tuple[Optional[str], str]:
        marker = cls.get_marker()
        parts = cls.key.split(marker)
        if len(parts) > 2:
            raise OptionException('Option declared with multi-namespace key `{}`.'.format(cls.key))
        if len(parts) == 1:
            return None, cls.key
        return parts[0], parts[1]

    @classmethod
    def get_namespace(cls) -> Optional[str]:
        return cls.parse_key()[0]

    @classmethod
    def get_key_subject(cls):
        return cls.parse_key()[1]

    @classmethod
    def to_dict(cls, value=None):
        return {
            'key': cls.key,
            'typing': cls.typing,
            'is_secret': cls.is_secret,
            'value': value or cls.default,
            'description': cls.description,
        }

    @classmethod
    def parse(cls, value):
        return parser.TYPE_MAPPING[cls.typing](
            key=cls.key,
            value=value,
            is_list=cls.is_list,
            is_optional=cls.is_optional,
            default=cls.default,
            options=cls.options)
