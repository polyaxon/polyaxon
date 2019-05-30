from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

K8S_SECRETS_BUILD_JOBS = '{}{}{}'.format(option_namespaces.K8S_SECRETS,
                                         NAMESPACE_DB_OPTION_MARKER,
                                         option_subjects.BUILD_JOBS)
K8S_SECRETS_JOBS = '{}{}{}'.format(option_namespaces.K8S_SECRETS,
                                   NAMESPACE_DB_OPTION_MARKER,
                                   option_subjects.JOBS)
K8S_SECRETS_EXPERIMENTS = '{}{}{}'.format(option_namespaces.K8S_SECRETS,
                                          NAMESPACE_DB_OPTION_MARKER,
                                          option_subjects.EXPERIMENTS)
K8S_SECRETS_NOTEBOOKS = '{}{}{}'.format(option_namespaces.K8S_SECRETS,
                                        NAMESPACE_DB_OPTION_MARKER,
                                        option_subjects.NOTEBOOKS)
K8S_SECRETS_TENSORBOARDS = '{}{}{}'.format(option_namespaces.K8S_SECRETS,
                                           NAMESPACE_DB_OPTION_MARKER,
                                           option_subjects.TENSORBOARDS)


class K8SSecretsBuildJobs(Option):
    key = K8S_SECRETS_BUILD_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'K8S secrets configuration for build jobs'


class K8SSecretsJobs(Option):
    key = K8S_SECRETS_JOBS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'K8S secrets configuration for jobs'


class K8SSecretsExperiments(Option):
    key = K8S_SECRETS_EXPERIMENTS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'K8S secrets configuration for experiments'


class K8SSecretsNotebooks(Option):
    key = K8S_SECRETS_NOTEBOOKS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'K8S secrets configuration for notebooks'


class K8SSecretsTensorboards(Option):
    key = K8S_SECRETS_TENSORBOARDS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'K8S secrets configuration for tensorboards'
