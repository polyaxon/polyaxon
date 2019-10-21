from typing import Optional, Tuple

from options.exceptions import OptionException
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.option_namespaces import FEATURES
from options.types import CONF_TYPES


class Feature(Option):
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.DB_OPTION
    typing = CONF_TYPES.BOOL
    default = True
    options = [True, False]
    immutable = False  # If immutable, the feature cannot be update by the user
    description = None

    @classmethod
    def get_marker(cls) -> str:
        return NAMESPACE_DB_OPTION_MARKER

    @classmethod
    def parse_key(cls) -> Tuple[Optional[str], str]:
        marker = cls.get_marker()
        parts = cls.key.split(marker)
        if len(parts) > 3 or len(parts) < 1:  # First part is a Meta namespace `features`
            raise OptionException('Feature declared with multi-namespace key `{}`.'.format(cls.key))
        if parts[0] != FEATURES:
            raise OptionException('Feature declared with wrong namespace key `{}`.'.format(cls.key))
        if len(parts) == 2:
            return None, parts[1]
        return parts[1], parts[2]

    @classmethod
    def get_namespace(cls) -> Optional[str]:
        return cls.parse_key()[0]

    @classmethod
    def get_key_subject(cls):
        return cls.parse_key()[1]
