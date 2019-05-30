from options import option_namespaces, option_subjects
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


class TolerationsBuildJobs(Option):
    key = TOLERATIONS_BUILD_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Tolerations configuration for build jobs'


class TolerationsJobs(Option):
    key = TOLERATIONS_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Tolerations configuration for jobs'


class TolerationsExperiments(Option):
    key = TOLERATIONS_EXPERIMENTS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Tolerations configuration for experiments'


class TolerationsNotebooks(Option):
    key = TOLERATIONS_NOTEBOOKS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Tolerations configuration for notebooks'


class TolerationsTensorboards(Option):
    key = TOLERATIONS_TENSORBOARDS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Tolerations configuration for tensorboards'
