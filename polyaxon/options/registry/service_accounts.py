from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

SERVICE_ACCOUNTS_BUILD_JOBS = '{}{}{}'.format(option_namespaces.SERVICE_ACCOUNTS,
                                              NAMESPACE_DB_OPTION_MARKER,
                                              option_subjects.BUILD_JOBS)
SERVICE_ACCOUNTS_JOBS = '{}{}{}'.format(option_namespaces.SERVICE_ACCOUNTS,
                                        NAMESPACE_DB_OPTION_MARKER,
                                        option_subjects.JOBS)
SERVICE_ACCOUNTS_EXPERIMENTS = '{}{}{}'.format(option_namespaces.SERVICE_ACCOUNTS,
                                               NAMESPACE_DB_OPTION_MARKER,
                                               option_subjects.EXPERIMENTS)
SERVICE_ACCOUNTS_NOTEBOOKS = '{}{}{}'.format(option_namespaces.SERVICE_ACCOUNTS,
                                             NAMESPACE_DB_OPTION_MARKER,
                                             option_subjects.NOTEBOOKS)
SERVICE_ACCOUNTS_TENSORBOARDS = '{}{}{}'.format(option_namespaces.SERVICE_ACCOUNTS,
                                                NAMESPACE_DB_OPTION_MARKER,
                                                option_subjects.TENSORBOARDS)


class ServiceAccountsBuildJobs(Option):
    key = SERVICE_ACCOUNTS_BUILD_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Service account configuration for build jobs'


class ServiceAccountsJobs(Option):
    key = SERVICE_ACCOUNTS_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Service account configuration for jobs'


class ServiceAccountsExperiments(Option):
    key = SERVICE_ACCOUNTS_EXPERIMENTS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Service account configuration for experiments'


class ServiceAccountsNotebooks(Option):
    key = SERVICE_ACCOUNTS_NOTEBOOKS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Service account configuration for notebooks'


class ServiceAccountsTensorboards(Option):
    key = SERVICE_ACCOUNTS_TENSORBOARDS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Service account configuration for tensorboards'
