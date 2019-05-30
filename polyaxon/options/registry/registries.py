from options.option import Option, OptionStores
from options.types import CONF_TYPES

REGISTRY_IN_CLUSTER = 'REGISTRY_IN_CLUSTER'
REGISTRY_LOCALHOST = 'REGISTRY_LOCALHOST'
REGISTRY_HOST = 'REGISTRY_HOST'


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


class RegistryLocalHost(Option):
    key = REGISTRY_LOCALHOST
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class RegistryHost(Option):
    key = REGISTRY_HOST
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None
