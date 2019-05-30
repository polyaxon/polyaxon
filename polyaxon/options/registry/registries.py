from options.option import Option, OptionStores
from options.types import CONF_TYPES

REGISTRY_IN_CLUSTER = 'REGISTRY_IN_CLUSTER'
REGISTRY_USER = 'REGISTRY_USER'
REGISTRY_PASSWORD = 'REGISTRY_PASSWORD'  # noqa
REGISTRY_LOCAL_URI = 'REGISTRY_LOCAL_URI'
REGISTRY_URI = 'REGISTRY_URI'


class RegistryInCluster(Option):
    key = REGISTRY_IN_CLUSTER
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.BOOL
    default = None
    options = None


class RegistryUser(Option):
    key = REGISTRY_USER
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class RegistryPassword(Option):
    key = REGISTRY_PASSWORD
    is_global = True
    is_secret = True
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class RegistryLocalUri(Option):
    key = REGISTRY_LOCAL_URI
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class RegistryUri(Option):
    key = REGISTRY_URI
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None
