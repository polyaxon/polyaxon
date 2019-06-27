from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

MAX_RESTARTS_BUILD_JOBS = '{}{}{}'.format(option_namespaces.MAX_RESTARTS,
                                          NAMESPACE_DB_OPTION_MARKER,
                                          option_subjects.BUILD_JOBS)
MAX_RESTARTS_JOBS = '{}{}{}'.format(option_namespaces.MAX_RESTARTS,
                                    NAMESPACE_DB_OPTION_MARKER,
                                    option_subjects.JOBS)
MAX_RESTARTS_EXPERIMENTS = '{}{}{}'.format(option_namespaces.MAX_RESTARTS,
                                           NAMESPACE_DB_OPTION_MARKER,
                                           option_subjects.EXPERIMENTS)
MAX_RESTARTS_NOTEBOOKS = '{}{}{}'.format(option_namespaces.MAX_RESTARTS,
                                         NAMESPACE_DB_OPTION_MARKER,
                                         option_subjects.NOTEBOOKS)
MAX_RESTARTS_TENSORBOARDS = '{}{}{}'.format(option_namespaces.MAX_RESTARTS,
                                            NAMESPACE_DB_OPTION_MARKER,
                                            option_subjects.TENSORBOARDS)


class MaxRestartsOption(Option):
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 0
    options = None


class MaxRestartsBuildJobs(MaxRestartsOption):
    key = MAX_RESTARTS_BUILD_JOBS
    description = 'Max restarts configuration for build jobs'


class MaxRestartsJobs(MaxRestartsOption):
    key = MAX_RESTARTS_JOBS
    description = 'Max restarts configuration for jobs'


class MaxRestartsExperiments(MaxRestartsOption):
    key = MAX_RESTARTS_EXPERIMENTS
    description = 'Max restarts configuration for experiments'


class MaxRestartsNotebooks(MaxRestartsOption):
    key = MAX_RESTARTS_NOTEBOOKS
    description = 'Max restarts configuration for notebooks'


class MaxRestartsTensorboards(MaxRestartsOption):
    key = MAX_RESTARTS_TENSORBOARDS
    description = 'Max restarts configuration for tensorboards'
