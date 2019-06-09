from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

K8S_RESOURCES_BUILD_JOBS = '{}{}{}'.format(option_namespaces.K8S_RESOURCES,
                                           NAMESPACE_DB_OPTION_MARKER,
                                           option_subjects.BUILD_JOBS)
K8S_RESOURCES_JOBS = '{}{}{}'.format(option_namespaces.K8S_RESOURCES,
                                     NAMESPACE_DB_OPTION_MARKER,
                                     option_subjects.JOBS)
K8S_RESOURCES_EXPERIMENTS = '{}{}{}'.format(option_namespaces.K8S_RESOURCES,
                                            NAMESPACE_DB_OPTION_MARKER,
                                            option_subjects.EXPERIMENTS)
K8S_RESOURCES_NOTEBOOKS = '{}{}{}'.format(option_namespaces.K8S_RESOURCES,
                                          NAMESPACE_DB_OPTION_MARKER,
                                          option_subjects.NOTEBOOKS)
K8S_RESOURCES_TENSORBOARDS = '{}{}{}'.format(option_namespaces.K8S_RESOURCES,
                                             NAMESPACE_DB_OPTION_MARKER,
                                             option_subjects.TENSORBOARDS)


class K8SResourcesBuildJobs(Option):
    key = K8S_RESOURCES_BUILD_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'K8S resources configuration for build jobs'


class K8SResourcesJobs(Option):
    key = K8S_RESOURCES_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'K8S resources configuration for jobs'


class K8SResourcesExperiments(Option):
    key = K8S_RESOURCES_EXPERIMENTS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'K8S resources configuration for experiments'


class K8SResourcesNotebooks(Option):
    key = K8S_RESOURCES_NOTEBOOKS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'K8S resources configuration for notebooks'


class K8SResourcesTensorboards(Option):
    key = K8S_RESOURCES_TENSORBOARDS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'K8S resources configuration for tensorboards'
