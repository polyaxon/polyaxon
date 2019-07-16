from options import option_namespaces, option_subjects
from options.cache import FREQUENT_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

AUTH_GITLAB_ENABLED = '{}{}{}'.format(option_namespaces.AUTH_GITLAB,
                                      NAMESPACE_DB_OPTION_MARKER,
                                      option_subjects.ENABLED)
AUTH_GITLAB_VERIFICATION_SCHEDULE = '{}{}{}'.format(option_namespaces.AUTH_GITLAB,
                                                    NAMESPACE_DB_OPTION_MARKER,
                                                    option_subjects.VERIFICATION_SCHEDULE)
AUTH_GITLAB_URL = '{}{}{}'.format(option_namespaces.AUTH_GITLAB,
                                  NAMESPACE_DB_OPTION_MARKER,
                                  option_subjects.URL)
AUTH_GITLAB_CLIENT_ID = '{}{}{}'.format(option_namespaces.AUTH_GITLAB,
                                        NAMESPACE_DB_OPTION_MARKER,
                                        option_subjects.CLIENT_ID)
AUTH_GITLAB_CLIENT_SECRET = '{}{}{}'.format(option_namespaces.AUTH_GITLAB,  # noqa
                                            NAMESPACE_DB_OPTION_MARKER,
                                            option_subjects.CLIENT_SECRET)


class AuthGitlabEnabled(Option):
    key = AUTH_GITLAB_ENABLED
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.BOOL
    store = OptionStores.DB_OPTION
    default = False
    options = None
    cache_ttl = FREQUENT_CACHE_TTL


class AuthGitlabVerificationSchedule(Option):
    key = AUTH_GITLAB_VERIFICATION_SCHEDULE
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 0
    options = None
    cache_ttl = FREQUENT_CACHE_TTL


class AuthGitlabUrl(Option):
    key = AUTH_GITLAB_URL
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    cache_ttl = FREQUENT_CACHE_TTL


class AuthGitlabClientId(Option):
    key = AUTH_GITLAB_CLIENT_ID
    is_global = True
    is_secret = True
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    cache_ttl = FREQUENT_CACHE_TTL


class AuthGitlabClientSecret(Option):
    key = AUTH_GITLAB_CLIENT_SECRET
    is_global = True
    is_secret = True
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    cache_ttl = FREQUENT_CACHE_TTL
