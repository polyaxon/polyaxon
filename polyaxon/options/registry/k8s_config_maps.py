from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

K8S_CONFIG_MAPS_BUILD_JOBS = '{}{}{}'.format(option_namespaces.K8S_CONFIG_MAPS,
                                             NAMESPACE_DB_OPTION_MARKER,
                                             option_subjects.BUILD_JOBS)
K8S_CONFIG_MAPS_JOBS = '{}{}{}'.format(option_namespaces.K8S_CONFIG_MAPS,
                                       NAMESPACE_DB_OPTION_MARKER,
                                       option_subjects.JOBS)
K8S_CONFIG_MAPS_EXPERIMENTS = '{}{}{}'.format(option_namespaces.K8S_CONFIG_MAPS,
                                              NAMESPACE_DB_OPTION_MARKER,
                                              option_subjects.EXPERIMENTS)
K8S_CONFIG_MAPS_NOTEBOOKS = '{}{}{}'.format(option_namespaces.K8S_CONFIG_MAPS,
                                            NAMESPACE_DB_OPTION_MARKER,
                                            option_subjects.NOTEBOOKS)
K8S_CONFIG_MAPS_TENSORBOARDS = '{}{}{}'.format(option_namespaces.K8S_CONFIG_MAPS,
                                               NAMESPACE_DB_OPTION_MARKER,
                                               option_subjects.TENSORBOARDS)


class K8SConfigMapsBuildJobs(Option):
    key = K8S_CONFIG_MAPS_BUILD_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None


class K8SConfigMapsJobs(Option):
    key = K8S_CONFIG_MAPS_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None


class K8SConfigMapsExperiments(Option):
    key = K8S_CONFIG_MAPS_EXPERIMENTS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None


class K8SConfigMapsNotebooks(Option):
    key = K8S_CONFIG_MAPS_NOTEBOOKS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None


class K8SConfigMapsTensorboards(Option):
    key = K8S_CONFIG_MAPS_TENSORBOARDS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
