from options import option_namespaces, option_subjects
from options.cache import FREQUENT_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

TOLERATIONS_BUILD_JOBS = '{}{}{}'.format(option_namespaces.TOLERATIONS,
                                         NAMESPACE_DB_OPTION_MARKER,
                                         option_subjects.BUILD_JOBS)
TOLERATIONS_JOBS = '{}{}{}'.format(option_namespaces.TOLERATIONS,
                                   NAMESPACE_DB_OPTION_MARKER,
                                   option_subjects.JOBS)
TOLERATIONS_EXPERIMENTS = '{}{}{}'.format(option_namespaces.TOLERATIONS,
                                          NAMESPACE_DB_OPTION_MARKER,
                                          option_subjects.EXPERIMENTS)
TOLERATIONS_NOTEBOOKS = '{}{}{}'.format(option_namespaces.TOLERATIONS,
                                        NAMESPACE_DB_OPTION_MARKER,
                                        option_subjects.NOTEBOOKS)
TOLERATIONS_TENSORBOARDS = '{}{}{}'.format(option_namespaces.TOLERATIONS,
                                           NAMESPACE_DB_OPTION_MARKER,
                                           option_subjects.TENSORBOARDS)


class TolerationsOption(Option):
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    cache_ttl = FREQUENT_CACHE_TTL


class TolerationsBuildJobs(TolerationsOption):
    key = TOLERATIONS_BUILD_JOBS
    description = 'Tolerations configuration for build jobs'


class TolerationsJobs(TolerationsOption):
    key = TOLERATIONS_JOBS
    description = 'Tolerations configuration for jobs'


class TolerationsExperiments(TolerationsOption):
    key = TOLERATIONS_EXPERIMENTS
    description = 'Tolerations configuration for experiments'


class TolerationsNotebooks(TolerationsOption):
    key = TOLERATIONS_NOTEBOOKS
    description = 'Tolerations configuration for notebooks'


class TolerationsTensorboards(TolerationsOption):
    key = TOLERATIONS_TENSORBOARDS
    description = 'Tolerations configuration for tensorboards'
