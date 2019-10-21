from options import option_namespaces, option_subjects
from options.cache import FREQUENT_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

ACCESS_GIT = '{}{}{}'.format(option_namespaces.ACCESS,
                             NAMESPACE_DB_OPTION_MARKER,
                             option_subjects.GIT)

ACCESS_REGISTRY = '{}{}{}'.format(option_namespaces.ACCESS,
                                  NAMESPACE_DB_OPTION_MARKER,
                                  option_subjects.REGISTRY)


class AccessGit(Option):
    key = ACCESS_GIT
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    cache_ttl = FREQUENT_CACHE_TTL


class AccessRegistry(Option):
    key = ACCESS_REGISTRY
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    cache_ttl = FREQUENT_CACHE_TTL
