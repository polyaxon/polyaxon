from options.option import Option, OptionStores
from options.types import CONF_TYPES

ALLOW_USER_PROJECTS = 'ALLOW_USER_PROJECTS'
OWNER_TYPES = 'OWNER_TYPES'
ROLES = 'ROLES'
DEFAULT_ROLE = 'DEFAULT_ROLE'
SCOPE_ROLES = 'SCOPE_ROLES'


class AllowUserProjects(Option):
    key = ALLOW_USER_PROJECTS
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.DB
    typing = CONF_TYPES.BOOL
    default = True
    options = None


class OwnerTypes(Option):
    key = OWNER_TYPES
    is_global = True
    is_secret = False
    is_optional = True
    is_list = True
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class Roles(Option):
    key = ROLES
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.DICT
    default = None
    options = None


class DefaultRole(Option):
    key = DEFAULT_ROLE
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class ScopeRoles(Option):
    key = SCOPE_ROLES
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.DICT_OF_DICTS
    default = None
    options = None
