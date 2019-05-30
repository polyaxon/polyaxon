from options.option import Option, OptionStores
from options.types import CONF_TYPES

PASSWORD_LENGTH = 'PASSWORD_LENGTH'  # noqa
ADMIN_VIEW_ENABLED = 'ADMIN_VIEW_ENABLED'
LOGGING = 'LOGGING'
DEBUG = 'DEBUG'
PROTOCOL = 'PROTOCOL'
API_HOST = 'API_HOST'
LOGIN_URL = 'LOGIN_URL'
ACCOUNT_ACTIVATION_DAYS = 'ACCOUNT_ACTIVATION_DAYS'
CELERY_BROKER_BACKEND = 'CELERY_BROKER_BACKEND'
CELERY_BROKER_URL = 'CELERY_BROKER_URL'
HEADERS_INTERNAL = 'HEADERS_INTERNAL'
SECRET_INTERNAL_TOKEN = 'SECRET_INTERNAL_TOKEN'  # noqa
HEALTH_CHECK_WORKER_TIMEOUT = 'HEALTH_CHECK_WORKER_TIMEOUT'
CLUSTER_NOTIFICATION_ALIVE_URL = 'CLUSTER_NOTIFICATION_ALIVE_URL'
CLUSTER_NOTIFICATION_URL = 'CLUSTER_NOTIFICATION_URL'
CLUSTER_NOTIFICATION_NODES_URL = 'CLUSTER_NOTIFICATION_NODES_URL'
SECURITY_CONTEXT_USER = 'SECURITY_CONTEXT_USER'
SECURITY_CONTEXT_GROUP = 'SECURITY_CONTEXT_GROUP'
ENCRYPTION_KEY = 'ENCRYPTION_KEY'
ENCRYPTION_SECRET = 'ENCRYPTION_SECRET'  # noqa


class PasswordLength(Option):
    key = PASSWORD_LENGTH
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.DB
    typing = CONF_TYPES.INT
    default = 8
    options = None


class AdminViewEnabled(Option):
    key = ADMIN_VIEW_ENABLED
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.BOOL
    default = True
    options = None


class Logging(Option):
    key = LOGGING
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.DICT
    default = None
    options = None


class Debug(Option):
    key = DEBUG
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.DICT
    default = None
    options = None


class Protocol(Option):
    key = PROTOCOL
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class ApiHost(Option):
    key = API_HOST
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class LoginUrl(Option):
    key = LOGIN_URL
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class AccountActivationDays(Option):
    key = ACCOUNT_ACTIVATION_DAYS
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.INT
    default = None
    options = None


class CeleryBrokerBackend(Option):
    key = CELERY_BROKER_BACKEND
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class CeleryBrokerUrl(Option):
    key = CELERY_BROKER_URL
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class HeadersInternal(Option):
    key = HEADERS_INTERNAL
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class SecretInternalToken(Option):
    key = SECRET_INTERNAL_TOKEN
    is_global = True
    is_secret = True
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class HealthCheckWorkerTimeout(Option):
    key = HEALTH_CHECK_WORKER_TIMEOUT
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.DB
    typing = CONF_TYPES.INT
    default = 4
    options = None


class ClusterNotificationAliveUrl(Option):
    key = CLUSTER_NOTIFICATION_ALIVE_URL
    is_global = True
    is_secret = True
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class ClusterNotificationUrl(Option):
    key = CLUSTER_NOTIFICATION_URL
    is_global = True
    is_secret = True
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class ClusterNotificationNodesUrl(Option):
    key = CLUSTER_NOTIFICATION_NODES_URL
    is_global = True
    is_secret = True
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class SecurityContextUser(Option):
    key = SECURITY_CONTEXT_USER
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class SecurityContextGroup(Option):
    key = SECURITY_CONTEXT_GROUP
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class EncryptionKey(Option):
    key = ENCRYPTION_KEY
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class EncryptionSecret(Option):
    key = ENCRYPTION_SECRET
    is_global = True
    is_secret = True
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None
