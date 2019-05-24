from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_MARKER, Option, OptionStores
from options.types import CONF_TYPES

AUTH_GITHUB_ENABLED = '{}{}{}'.format(option_namespaces.AUTH_GITHUB,
                                      NAMESPACE_DB_MARKER,
                                      option_subjects.ENABLED)
AUTH_GITHUB_VERIFICATION_SCHEDULE = '{}{}{}'.format(option_namespaces.AUTH_GITHUB,
                                                    NAMESPACE_DB_MARKER,
                                                    option_subjects.VERIFICATION_SCHEDULE)
AUTH_GITHUB_CLIENT_ID = '{}{}{}'.format(option_namespaces.AUTH_GITHUB,
                                        NAMESPACE_DB_MARKER,
                                        option_subjects.CLIENT_ID)
AUTH_GITHUB_CLIENT_SECRET = '{}{}{}'.format(option_namespaces.AUTH_GITHUB,
                                            NAMESPACE_DB_MARKER,
                                            option_subjects.CLIENT_SECRET)


class AuthGithubEnabled(Option):
    key = AUTH_GITHUB_ENABLED
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.BOOL
    store = OptionStores.DB
    default = False
    options = None


class AuthGithubVerificationSchedule(Option):
    key = AUTH_GITHUB_VERIFICATION_SCHEDULE
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB
    default = 0
    options = None


class AuthGithubClientId(Option):
    key = AUTH_GITHUB_CLIENT_ID
    is_global = True
    is_secret = True
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB
    default = None
    options = None


class AuthGithubClientSecret(Option):
    key = AUTH_GITHUB_CLIENT_SECRET
    is_global = True
    is_secret = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB
    default = None
    options = None
