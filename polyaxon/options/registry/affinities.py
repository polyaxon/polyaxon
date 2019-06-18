from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

AFFINITIES_BUILD_JOBS = '{}{}{}'.format(option_namespaces.AFFINITIES,
                                        NAMESPACE_DB_OPTION_MARKER,
                                        option_subjects.BUILD_JOBS)
AFFINITIES_JOBS = '{}{}{}'.format(option_namespaces.AFFINITIES,
                                  NAMESPACE_DB_OPTION_MARKER,
                                  option_subjects.JOBS)
AFFINITIES_EXPERIMENTS = '{}{}{}'.format(option_namespaces.AFFINITIES,
                                         NAMESPACE_DB_OPTION_MARKER,
                                         option_subjects.EXPERIMENTS)
AFFINITIES_NOTEBOOKS = '{}{}{}'.format(option_namespaces.AFFINITIES,
                                       NAMESPACE_DB_OPTION_MARKER,
                                       option_subjects.NOTEBOOKS)
AFFINITIES_TENSORBOARDS = '{}{}{}'.format(option_namespaces.AFFINITIES,
                                          NAMESPACE_DB_OPTION_MARKER,
                                          option_subjects.TENSORBOARDS)


class AffinitiesOption(Option):
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None


class AffinitiesBuildJobs(AffinitiesOption):
    key = AFFINITIES_BUILD_JOBS
    description = 'Affinity configuration for build jobs'


class AffinitiesJobs(AffinitiesOption):
    key = AFFINITIES_JOBS
    description = 'Affinity configuration for jobs'


class AffinitiesExperiments(AffinitiesOption):
    key = AFFINITIES_EXPERIMENTS
    description = 'Affinity configuration for experiments'


class AffinitiesNotebooks(AffinitiesOption):
    key = AFFINITIES_NOTEBOOKS
    description = 'Affinity configuration for notebooks'


class AffinitiesTensorboards(AffinitiesOption):
    key = AFFINITIES_TENSORBOARDS
    description = 'Affinity configuration for tensorboards'
