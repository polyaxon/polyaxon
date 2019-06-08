from options.option import Option, OptionStores
from options.types import CONF_TYPES

REPOS_CLAIM_NAME = 'REPOS_CLAIM_NAME'
REPOS_HOST_PATH = 'REPOS_HOST_PATH'
REPOS_MOUNT_PATH = 'REPOS_MOUNT_PATH'

UPLOAD_MOUNT_PATH = 'UPLOAD_MOUNT_PATH'

PERSISTENCE_DATA = 'PERSISTENCE_DATA'
PERSISTENCE_OUTPUTS = 'PERSISTENCE_OUTPUTS'
PERSISTENCE_LOGS = 'PERSISTENCE_LOGS'


class ReposClaimName(Option):
    key = REPOS_CLAIM_NAME
    is_global = False
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class ReposHostPath(Option):
    key = REPOS_HOST_PATH
    is_global = False
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class ReposMountPath(Option):
    key = REPOS_MOUNT_PATH
    is_global = False
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class UploadMountPath(Option):
    key = UPLOAD_MOUNT_PATH
    is_global = False
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class PersistenceData(Option):
    key = PERSISTENCE_DATA
    is_global = False
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.DICT
    default = None
    options = None


class PersistenceOutputs(Option):
    key = PERSISTENCE_OUTPUTS
    is_global = False
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.DICT
    default = None
    options = None


class PersistenceLogs(Option):
    key = PERSISTENCE_LOGS
    is_global = False
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.DICT
    default = None
    options = None
