from options.option import Option, OptionStores
from options.types import CONF_TYPES

POLYAXON_ENVIRONMENT = 'POLYAXON_ENVIRONMENT'
CHART_VERSION = 'CHART_VERSION'
CHART_IS_UPGRADE = 'CHART_IS_UPGRADE'
CLI_MIN_VERSION = 'CLI_MIN_VERSION'
CLI_LATEST_VERSION = 'CLI_LATEST_VERSION'
PLATFORM_MIN_VERSION = 'PLATFORM_MIN_VERSION'
PLATFORM_LATEST_VERSION = 'PLATFORM_LATEST_VERSION'
LIB_MIN_VERSION = 'LIB_MIN_VERSION'
LIB_LATEST_VERSION = 'LIB_LATEST_VERSION'


class PlatformEnvironmentVersion(Option):
    key = POLYAXON_ENVIRONMENT
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class ChartVersion(Option):
    key = CHART_VERSION
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class ChartIsUpgrade(Option):
    key = CHART_IS_UPGRADE
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.BOOL
    store = OptionStores.SETTINGS
    default = None
    options = None


class CliMinVersion(Option):
    key = CLI_MIN_VERSION
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class CliLatestVersion(Option):
    key = CLI_LATEST_VERSION
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class PlatformMinVersion(Option):
    key = PLATFORM_MIN_VERSION
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class PlatformLatestVersion(Option):
    key = PLATFORM_LATEST_VERSION
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class LibMinVersion(Option):
    key = LIB_MIN_VERSION
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class LibLatestVersion(Option):
    key = LIB_LATEST_VERSION
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None
