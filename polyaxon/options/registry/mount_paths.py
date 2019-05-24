from options.option import Option, OptionStores
from options.types import CONF_TYPES

MOUNT_PATHS_NVIDIA = 'MOUNT_PATHS_NVIDIA'
DIRS_NVIDIA = 'DIRS_NVIDIA'


class MountPathsNvidia(Option):
    key = MOUNT_PATHS_NVIDIA
    is_global = False
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.DICT
    default = None
    options = None
    description = 'Configuration for Nvidia paths'


class DirsNvidia(Option):
    key = DIRS_NVIDIA
    is_global = False
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.DICT
    default = None
    options = None
    description = 'Configuration for exposing Nvidia from host nodes'
