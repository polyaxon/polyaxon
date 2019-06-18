from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

AUTH_BITBUCKET_ENABLED = '{}{}{}'.format(option_namespaces.AUTH_BITBUCKET,
                                         NAMESPACE_DB_OPTION_MARKER,
                                         option_subjects.ENABLED)
AUTH_BITBUCKET_VERIFICATION_SCHEDULE = '{}{}{}'.format(option_namespaces.AUTH_BITBUCKET,
                                                       NAMESPACE_DB_OPTION_MARKER,
                                                       option_subjects.VERIFICATION_SCHEDULE)
AUTH_BITBUCKET_CLIENT_ID = '{}{}{}'.format(option_namespaces.AUTH_BITBUCKET,
                                           NAMESPACE_DB_OPTION_MARKER,
                                           option_subjects.CLIENT_ID)
AUTH_BITBUCKET_CLIENT_SECRET = '{}{}{}'.format(option_namespaces.AUTH_BITBUCKET,  # noqa
                                               NAMESPACE_DB_OPTION_MARKER,
                                               option_subjects.CLIENT_SECRET)


class AuthBitbucketEnabled(Option):
    key = AUTH_BITBUCKET_ENABLED
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.BOOL
    store = OptionStores.DB_OPTION
    default = False
    options = None


class AuthBitbucketVerificationSchedule(Option):
    key = AUTH_BITBUCKET_VERIFICATION_SCHEDULE
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 0
    options = None


class AuthBitbucketClientId(Option):
    key = AUTH_BITBUCKET_CLIENT_ID
    is_global = True
    is_secret = True
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None


class AuthBitbucketClientSecret(Option):
    key = AUTH_BITBUCKET_CLIENT_SECRET
    is_global = True
    is_secret = True
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
