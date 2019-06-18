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

RESTRICT_K8S_RESOURCES = 'RESTRICT_K8S_RESOURCES'


class LabelsOption(Option):
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    store = OptionStores.SETTINGS
    typing = CONF_TYPES.STR
    default = None
    options = None


class RoleLabelsWorker(LabelsOption):
    key = ROLE_LABELS_WORKER


class RoleLabelsDashboard(LabelsOption):
    key = ROLE_LABELS_DASHBOARD


class RoleLabelsLog(LabelsOption):
    key = ROLE_LABELS_LOG


class RoleLabelsApi(LabelsOption):
    key = ROLE_LABELS_API


class RoleLabelsConfig(LabelsOption):
    key = ROLE_LABELS_CONFIG


class RoleLabelsHooks(LabelsOption):
    key = ROLE_LABELS_HOOKS


class TypeLabelsCore(LabelsOption):
    key = TYPE_LABELS_CORE


class TypeLabelsRunner(LabelsOption):
    key = TYPE_LABELS_RUNNER


class AppLabelsTensorboard(LabelsOption):
    key = APP_LABELS_TENSORBOARD


class AppLabelsNotebook(LabelsOption):
    key = APP_LABELS_NOTEBOOK


class AppLabelsDockerizer(LabelsOption):
    key = APP_LABELS_DOCKERIZER


class AppLabelsExperiment(LabelsOption):
    key = APP_LABELS_EXPERIMENT


class AppLabelsJob(LabelsOption):
    key = APP_LABELS_JOB


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


class RestrictK8SResources(Option):
    key = RESTRICT_K8S_RESOURCES
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    store = OptionStores.DB_OPTION
    typing = CONF_TYPES.BOOL
    default = True
    options = None
    description = ("Whether or not to all the user to mount any resource "
                   "without validating against the resource catalog.")
