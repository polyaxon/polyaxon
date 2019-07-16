from options import option_namespaces, option_subjects
from options.cache import FREQUENT_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

ANNOTATIONS_BUILD_JOBS = '{}{}{}'.format(option_namespaces.ANNOTATIONS,
                                         NAMESPACE_DB_OPTION_MARKER,
                                         option_subjects.BUILD_JOBS)
ANNOTATIONS_JOBS = '{}{}{}'.format(option_namespaces.ANNOTATIONS,
                                   NAMESPACE_DB_OPTION_MARKER,
                                   option_subjects.JOBS)
ANNOTATIONS_EXPERIMENTS = '{}{}{}'.format(option_namespaces.ANNOTATIONS,
                                          NAMESPACE_DB_OPTION_MARKER,
                                          option_subjects.EXPERIMENTS)
ANNOTATIONS_NOTEBOOKS = '{}{}{}'.format(option_namespaces.ANNOTATIONS,
                                        NAMESPACE_DB_OPTION_MARKER,
                                        option_subjects.NOTEBOOKS)
ANNOTATIONS_TENSORBOARDS = '{}{}{}'.format(option_namespaces.ANNOTATIONS,
                                           NAMESPACE_DB_OPTION_MARKER,
                                           option_subjects.TENSORBOARDS)


class AnnotationsOption(Option):
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    cache_ttl = FREQUENT_CACHE_TTL


class AnnotationsBuildJobs(AnnotationsOption):
    key = ANNOTATIONS_BUILD_JOBS
    description = 'Annotations configuration for build jobs'


class AnnotationsJobs(AnnotationsOption):
    key = ANNOTATIONS_JOBS
    description = 'Annotations configuration for jobs'


class AnnotationsExperiments(AnnotationsOption):
    key = ANNOTATIONS_EXPERIMENTS
    description = 'Annotations configuration for experiments'


class AnnotationsNotebooks(AnnotationsOption):
    key = ANNOTATIONS_NOTEBOOKS
    description = 'Annotations configuration for notebooks'


class AnnotationsTensorboards(AnnotationsOption):
    key = ANNOTATIONS_TENSORBOARDS
    description = 'Annotations configuration for tensorboards'
