from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

K8S_NAMESPACE = 'K8S_NAMESPACE'
K8S_CONFIG = 'K8S_CONFIG'
K8S_NODE_NAME = 'K8S_NODE_NAME'
K8S_RBAC_ENABLED = 'K8S_RBAC_ENABLED'
K8S_INGRESS_ENABLED = 'K8S_INGRESS_ENABLED'
K8S_INGRESS_ANNOTATIONS = 'K8S_INGRESS_ANNOTATIONS'
K8S_SERVICE_ACCOUNT_NAME = 'K8S_SERVICE_ACCOUNT_NAME'
K8S_SERVICE_ACCOUNT_EXPERIMENTS = 'K8S_SERVICE_ACCOUNT_EXPERIMENTS'
K8S_SERVICE_ACCOUNT_JOBS = 'K8S_SERVICE_ACCOUNT_JOBS'
K8S_SERVICE_ACCOUNT_BUILDS = 'K8S_SERVICE_ACCOUNT_BUILDS'

K8S_GPU_RESOURCE_KEY = '{}{}{}'.format(option_namespaces.K8S,
                                       NAMESPACE_DB_OPTION_MARKER,
                                       option_subjects.GPU_RESOURCE_KEY)
K8S_TPU_TF_VERSION = '{}{}{}'.format(option_namespaces.K8S,
                                     NAMESPACE_DB_OPTION_MARKER,
                                     option_subjects.TPU_TF_VERSION)
K8S_TPU_RESOURCE_KEY = '{}{}{}'.format(option_namespaces.K8S,
                                       NAMESPACE_DB_OPTION_MARKER,
                                       option_subjects.TPU_RESOURCE_KEY)


class K8SNamespace(Option):
    key = K8S_NAMESPACE
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class K8SConfig(Option):
    key = K8S_CONFIG
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class K8SNodeName(Option):
    key = K8S_NODE_NAME
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class K8SRBACEnabled(Option):
    key = K8S_RBAC_ENABLED
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.BOOL
    store = OptionStores.SETTINGS
    default = None
    options = None


class K8SIngressEnabled(Option):
    key = K8S_INGRESS_ENABLED
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.BOOL
    store = OptionStores.SETTINGS
    default = None
    options = None


class K8SIngressAnnotations(Option):
    key = K8S_INGRESS_ANNOTATIONS
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class K8SServiceAccountName(Option):
    key = K8S_SERVICE_ACCOUNT_NAME
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class K8SServiceAccountExperiments(Option):
    key = K8S_SERVICE_ACCOUNT_EXPERIMENTS
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class K8SServiceAccountJobs(Option):
    key = K8S_SERVICE_ACCOUNT_JOBS
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class K8SServiceAccountBuilds(Option):
    key = K8S_SERVICE_ACCOUNT_BUILDS
    is_global = True
    is_secret = False
    is_optional = False
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.SETTINGS
    default = None
    options = None


class K8SGpuResourceKey(Option):
    key = K8S_GPU_RESOURCE_KEY
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = 'nvidia.com/gpu'
    options = None


class K8STpuTfVersion(Option):
    key = K8S_TPU_TF_VERSION
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = '1.12'
    options = None


class K8STpuResourceKey(Option):
    key = K8S_TPU_RESOURCE_KEY
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = 'cloud-tpus.google.com/v2'
    options = {'cloud-tpus.google.com/v2', 'cloud-tpus.google.com/preemptible-v2'}
