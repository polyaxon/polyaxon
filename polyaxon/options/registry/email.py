from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

EMAIL_DEFAULT_DOMAIN = '{}{}{}'.format(option_namespaces.EMAIL,
                                       NAMESPACE_DB_OPTION_MARKER,
                                       option_subjects.DEFAULT_DOMAIN)

DEFAULT_FROM_EMAIL = 'DEFAULT_FROM_EMAIL'
EMAIL_HOST_USER = 'EMAIL_HOST_USER'
EMAIL_HOST_PASSWORD = 'EMAIL_HOST_PASSWORD'  # noqa


class EmailDefaultDomain(Option):
    key = EMAIL_DEFAULT_DOMAIN
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = 'local_polyaxon.com'
    options = None


class DefaultFromEmail(Option):
    key = DEFAULT_FROM_EMAIL
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class EmailHostUser(Option):
    key = EMAIL_HOST_USER
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class EmailHostPassword(Option):
    key = EMAIL_HOST_PASSWORD
    is_global = True
    is_secret = True
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None
