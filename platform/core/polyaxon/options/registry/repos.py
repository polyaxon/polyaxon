from options import option_namespaces, option_subjects
from options.cache import FREQUENT_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

REPOS_ACCESS_TOKEN = '{}{}{}'.format(option_namespaces.REPOS,
                                     NAMESPACE_DB_OPTION_MARKER,
                                     option_subjects.ACCESS_TOKEN)

REPOS_CREDENTIALS = '{}{}{}'.format(option_namespaces.REPOS,
                                    NAMESPACE_DB_OPTION_MARKER,
                                    option_subjects.CREDENTIALS)


class ReposAccessToken(Option):
    key = REPOS_ACCESS_TOKEN
    is_global = False
    is_secret = True
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Access token to pull repos'
    cache_ttl = FREQUENT_CACHE_TTL


class ReposCredentials(Option):
    key = REPOS_CREDENTIALS
    is_global = False
    is_secret = True
    is_optional = True
    is_list = False
    typing = CONF_TYPES.AUTH
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Credentials (user:password) to pull repos'
    cache_ttl = FREQUENT_CACHE_TTL
