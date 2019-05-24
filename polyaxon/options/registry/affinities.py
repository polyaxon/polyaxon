from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_MARKER, Option, OptionStores
from options.types import CONF_TYPES

AFFINITIES_BUILD_JOBS = '{}{}{}'.format(option_namespaces.AFFINITIES,
                                        NAMESPACE_DB_MARKER,
                                        option_subjects.BUILD_JOBS)
AFFINITIES_JOBS = '{}{}{}'.format(option_namespaces.AFFINITIES,
                                  NAMESPACE_DB_MARKER,
                                  option_subjects.JOBS)
AFFINITIES_EXPERIMENTS = '{}{}{}'.format(option_namespaces.AFFINITIES,
                                         NAMESPACE_DB_MARKER,
                                         option_subjects.EXPERIMENTS)
AFFINITIES_NOTEBOOKS = '{}{}{}'.format(option_namespaces.AFFINITIES,
                                       NAMESPACE_DB_MARKER,
                                       option_subjects.NOTEBOOKS)
AFFINITIES_TENSORBOARDS = '{}{}{}'.format(option_namespaces.AFFINITIES,
                                          NAMESPACE_DB_MARKER,
                                          option_subjects.TENSORBOARDS)


class AffinitiesBuildJobs(Option):
    key = AFFINITIES_BUILD_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB
    default = None
    options = None
    description = 'Affinity configuration for build jobs'


class AffinitiesJobs(Option):
    key = AFFINITIES_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB
    default = None
    options = None
    description = 'Affinity configuration for jobs'


class AffinitiesExperiments(Option):
    key = AFFINITIES_EXPERIMENTS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB
    default = None
    options = None
    description = 'Affinity configuration for experiments'


class AffinitiesNotebooks(Option):
    key = AFFINITIES_NOTEBOOKS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB
    default = None
    options = None
    description = 'Affinity configuration for notebooks'


class AffinitiesTensorboards(Option):
    key = AFFINITIES_TENSORBOARDS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB
    default = None
    options = None
    description = 'Affinity configuration for tensorboards'
