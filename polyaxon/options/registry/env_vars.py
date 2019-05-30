from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

ENV_VARS_BUILD_JOBS = '{}{}{}'.format(option_namespaces.ENV_VARS,
                                      NAMESPACE_DB_OPTION_MARKER,
                                      option_subjects.BUILD_JOBS)
ENV_VARS_JOBS = '{}{}{}'.format(option_namespaces.ENV_VARS,
                                NAMESPACE_DB_OPTION_MARKER,
                                option_subjects.JOBS)
ENV_VARS_EXPERIMENTS = '{}{}{}'.format(option_namespaces.ENV_VARS,
                                       NAMESPACE_DB_OPTION_MARKER,
                                       option_subjects.EXPERIMENTS)
ENV_VARS_NOTEBOOKS = '{}{}{}'.format(option_namespaces.ENV_VARS,
                                     NAMESPACE_DB_OPTION_MARKER,
                                     option_subjects.NOTEBOOKS)
ENV_VARS_TENSORBOARDS = '{}{}{}'.format(option_namespaces.ENV_VARS,
                                        NAMESPACE_DB_OPTION_MARKER,
                                        option_subjects.TENSORBOARDS)


class EnvVarsBuildJobs(Option):
    key = ENV_VARS_BUILD_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.LIST
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Env vars configuration for build jobs'


class EnvVarsJobs(Option):
    key = ENV_VARS_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.LIST
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Env vars configuration for jobs'


class EnvVarsExperiments(Option):
    key = ENV_VARS_EXPERIMENTS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.LIST
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Env vars configuration for experiments'


class EnvVarsNotebooks(Option):
    key = ENV_VARS_NOTEBOOKS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.LIST
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Env vars configuration for notebooks'


class EnvVarsTensorboards(Option):
    key = ENV_VARS_TENSORBOARDS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.LIST
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Env vars configuration for tensorboards'
