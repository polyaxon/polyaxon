from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_MARKER, Option, OptionStores
from options.types import CONF_TYPES

NODE_SELECTORS_BUILD_JOBS = '{}{}{}'.format(option_namespaces.NODE_SELECTORS,
                                            NAMESPACE_DB_MARKER,
                                            option_subjects.BUILD_JOBS)
NODE_SELECTORS_JOBS = '{}{}{}'.format(option_namespaces.NODE_SELECTORS,
                                      NAMESPACE_DB_MARKER,
                                      option_subjects.JOBS)
NODE_SELECTORS_EXPERIMENTS = '{}{}{}'.format(option_namespaces.NODE_SELECTORS,
                                             NAMESPACE_DB_MARKER,
                                             option_subjects.EXPERIMENTS)
NODE_SELECTORS_NOTEBOOKS = '{}{}{}'.format(option_namespaces.NODE_SELECTORS,
                                           NAMESPACE_DB_MARKER,
                                           option_subjects.NOTEBOOKS)
NODE_SELECTORS_TENSORBOARDS = '{}{}{}'.format(option_namespaces.NODE_SELECTORS,
                                              NAMESPACE_DB_MARKER,
                                              option_subjects.TENSORBOARDS)


class NodeSelectorsBuildJobs(Option):
    key = NODE_SELECTORS_BUILD_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB
    default = None
    options = None
    description = 'Node selectors configuration for build jobs'


class NodeSelectorsJobs(Option):
    key = NODE_SELECTORS_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB
    default = None
    options = None
    description = 'Node selectors configuration for jobs'


class NodeSelectorsExperiments(Option):
    key = NODE_SELECTORS_EXPERIMENTS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB
    default = None
    options = None
    description = 'Node selectors configuration for experiments'


class NodeSelectorsNotebooks(Option):
    key = NODE_SELECTORS_NOTEBOOKS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB
    default = None
    options = None
    description = 'Node selectors configuration for notebooks'


class NodeSelectorsTensorboards(Option):
    key = NODE_SELECTORS_TENSORBOARDS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB
    default = None
    options = None
    description = 'Node selectors configuration for tensorboards'
