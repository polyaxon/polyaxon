from options import option_namespaces, option_subjects
from options.cache import FREQUENT_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

NODE_SELECTORS_BUILD_JOBS = '{}{}{}'.format(option_namespaces.NODE_SELECTORS,
                                            NAMESPACE_DB_OPTION_MARKER,
                                            option_subjects.BUILD_JOBS)
NODE_SELECTORS_JOBS = '{}{}{}'.format(option_namespaces.NODE_SELECTORS,
                                      NAMESPACE_DB_OPTION_MARKER,
                                      option_subjects.JOBS)
NODE_SELECTORS_EXPERIMENTS = '{}{}{}'.format(option_namespaces.NODE_SELECTORS,
                                             NAMESPACE_DB_OPTION_MARKER,
                                             option_subjects.EXPERIMENTS)
NODE_SELECTORS_NOTEBOOKS = '{}{}{}'.format(option_namespaces.NODE_SELECTORS,
                                           NAMESPACE_DB_OPTION_MARKER,
                                           option_subjects.NOTEBOOKS)
NODE_SELECTORS_TENSORBOARDS = '{}{}{}'.format(option_namespaces.NODE_SELECTORS,
                                              NAMESPACE_DB_OPTION_MARKER,
                                              option_subjects.TENSORBOARDS)


class NodeSelectorsOption(Option):
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    cache_ttl = FREQUENT_CACHE_TTL


class NodeSelectorsBuildJobs(NodeSelectorsOption):
    key = NODE_SELECTORS_BUILD_JOBS
    description = 'Node selectors configuration for build jobs'


class NodeSelectorsJobs(NodeSelectorsOption):
    key = NODE_SELECTORS_JOBS
    description = 'Node selectors configuration for jobs'


class NodeSelectorsExperiments(NodeSelectorsOption):
    key = NODE_SELECTORS_EXPERIMENTS
    description = 'Node selectors configuration for experiments'


class NodeSelectorsNotebooks(NodeSelectorsOption):
    key = NODE_SELECTORS_NOTEBOOKS
    description = 'Node selectors configuration for notebooks'


class NodeSelectorsTensorboards(NodeSelectorsOption):
    key = NODE_SELECTORS_TENSORBOARDS
    description = 'Node selectors configuration for tensorboards'
