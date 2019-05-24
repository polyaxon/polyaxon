from options.option import Option, OptionStores
from options.types import CONF_TYPES

ROLE_LABELS_WORKER = 'ROLE_LABELS_WORKER'
ROLE_LABELS_DASHBOARD = 'ROLE_LABELS_DASHBOARD'
ROLE_LABELS_LOG = 'ROLE_LABELS_LOG'
ROLE_LABELS_API = 'ROLE_LABELS_API'
ROLE_LABELS_CONFIG = 'ROLE_LABELS_CONFIG'
ROLE_LABELS_HOOKS = 'ROLE_LABELS_HOOKS'

TYPE_LABELS_CORE = 'TYPE_LABELS_CORE'
TYPE_LABELS_RUNNER = 'TYPE_LABELS_RUNNER'

APP_LABELS_TENSORBOARD = 'APP_LABELS_TENSORBOARD'
APP_LABELS_NOTEBOOK = 'APP_LABELS_NOTEBOOK'
APP_LABELS_DOCKERIZER = 'APP_LABELS_DOCKERIZER'
APP_LABELS_EXPERIMENT = 'APP_LABELS_EXPERIMENT'
APP_LABELS_JOB = 'APP_LABELS_JOB'

DNS_USE_RESOLVER = 'DNS_USE_RESOLVER'
DNS_CUSTOM_CLUSTER = 'DNS_CUSTOM_CLUSTER'

PLUGINS = 'PLUGINS'
PUBLIC_PLUGIN_JOBS = 'PUBLIC_PLUGIN_JOBS'

# TODO: Remove this once the validation is using the catalogs
REFS_CONFIG_MAPS = 'REFS_CONFIG_MAPS'
REFS_SECRETS = 'REFS_SECRETS'


class RoleLabelsWorker(Option):
    key = ROLE_LABELS_WORKER
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class RoleLabelsDashboard(Option):
    key = ROLE_LABELS_DASHBOARD
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class RoleLabelsLog(Option):
    key = ROLE_LABELS_LOG
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class RoleLabelsApi(Option):
    key = ROLE_LABELS_API
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class RoleLabelsConfig(Option):
    key = ROLE_LABELS_CONFIG
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class RoleLabelsHooks(Option):
    key = ROLE_LABELS_HOOKS
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class TypeLabelsCore(Option):
    key = TYPE_LABELS_CORE
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class TypeLabelsRunner(Option):
    key = TYPE_LABELS_RUNNER
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class AppLabelsTensorboard(Option):
    key = APP_LABELS_TENSORBOARD
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class AppLabelsNotebook(Option):
    key = APP_LABELS_NOTEBOOK
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class AppLabelsDockerizer(Option):
    key = APP_LABELS_DOCKERIZER
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class AppLabelsExperiment(Option):
    key = APP_LABELS_EXPERIMENT
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class AppLabelsJob(Option):
    key = APP_LABELS_JOB
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class DnsUseResolver(Option):
    key = DNS_USE_RESOLVER
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.BOOL
    default = None
    options = None


class DnsCustomCluster(Option):
    key = DNS_CUSTOM_CLUSTER
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class Plugins(Option):
    key = PLUGINS
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.DICT_OF_DICTS
    default = {}
    options = None


class PublicPluginJobs(Option):
    key = PUBLIC_PLUGIN_JOBS
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.BOOL
    default = None
    options = None


class RefsConfigMaps(Option):
    key = REFS_CONFIG_MAPS
    is_global = True
    is_secret = False
    is_optional = False
    is_list = True
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class RefsSecrets(Option):
    key = REFS_SECRETS
    is_global = True
    is_secret = False
    is_optional = False
    is_list = True
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None
