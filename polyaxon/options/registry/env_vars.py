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


class EnvVarsOption(Option):
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.LIST
    store = OptionStores.DB_OPTION
    default = None
    options = None


class EnvVarsBuildJobs(EnvVarsOption):
    key = ENV_VARS_BUILD_JOBS
    description = 'Env vars configuration for build jobs'


class EnvVarsJobs(EnvVarsOption):
    key = ENV_VARS_JOBS
    description = 'Env vars configuration for jobs'


class EnvVarsExperiments(EnvVarsOption):
    key = ENV_VARS_EXPERIMENTS
    description = 'Env vars configuration for experiments'


class EnvVarsNotebooks(EnvVarsOption):
    key = ENV_VARS_NOTEBOOKS
    description = 'Env vars configuration for notebooks'


class EnvVarsTensorboards(EnvVarsOption):
    key = ENV_VARS_TENSORBOARDS
    description = 'Env vars configuration for tensorboards'
