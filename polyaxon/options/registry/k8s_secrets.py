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


class K8SSecretsOption(Option):
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None


class K8SSecretsBuildJobs(K8SSecretsOption):
    key = K8S_SECRETS_BUILD_JOBS
    description = 'K8S secrets configuration for build jobs'


class K8SSecretsJobs(K8SSecretsOption):
    key = K8S_SECRETS_JOBS
    description = 'K8S secrets configuration for jobs'


class K8SSecretsExperiments(K8SSecretsOption):
    key = K8S_SECRETS_EXPERIMENTS
    description = 'K8S secrets configuration for experiments'


class K8SSecretsNotebooks(K8SSecretsOption):
    key = K8S_SECRETS_NOTEBOOKS
    description = 'K8S secrets configuration for notebooks'


class K8SSecretsTensorboards(K8SSecretsOption):
    key = K8S_SECRETS_TENSORBOARDS
    description = 'K8S secrets configuration for tensorboards'
