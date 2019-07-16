from options import option_namespaces, option_subjects
from options.cache import FREQUENT_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES
from schemas import PodResourcesConfig

K8S_RESOURCES_BUILD_JOBS = '{}{}{}'.format(option_namespaces.K8S_RESOURCES,
                                           NAMESPACE_DB_OPTION_MARKER,
                                           option_subjects.BUILD_JOBS)
K8S_RESOURCES_JOBS = '{}{}{}'.format(option_namespaces.K8S_RESOURCES,
                                     NAMESPACE_DB_OPTION_MARKER,
                                     option_subjects.JOBS)
K8S_RESOURCES_EXPERIMENTS = '{}{}{}'.format(option_namespaces.K8S_RESOURCES,
                                            NAMESPACE_DB_OPTION_MARKER,
                                            option_subjects.EXPERIMENTS)
K8S_RESOURCES_NOTEBOOKS = '{}{}{}'.format(option_namespaces.K8S_RESOURCES,
                                          NAMESPACE_DB_OPTION_MARKER,
                                          option_subjects.NOTEBOOKS)
K8S_RESOURCES_TENSORBOARDS = '{}{}{}'.format(option_namespaces.K8S_RESOURCES,
                                             NAMESPACE_DB_OPTION_MARKER,
                                             option_subjects.TENSORBOARDS)


class K8SResourcesOption(Option):
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.DICT
    store = OptionStores.DB_OPTION
    default = None
    options = None
    cache_ttl = FREQUENT_CACHE_TTL

    @classmethod
    def _extra_processing(cls, value):
        if not value:
            return value
        PodResourcesConfig.from_dict(value)
        return value


class K8SResourcesBuildJobs(K8SResourcesOption):
    key = K8S_RESOURCES_BUILD_JOBS
    description = 'K8S resources configuration for build jobs'


class K8SResourcesJobs(K8SResourcesOption):
    key = K8S_RESOURCES_JOBS
    description = 'K8S resources configuration for jobs'


class K8SResourcesExperiments(K8SResourcesOption):
    key = K8S_RESOURCES_EXPERIMENTS
    description = 'K8S resources configuration for experiments'


class K8SResourcesNotebooks(K8SResourcesOption):
    key = K8S_RESOURCES_NOTEBOOKS
    description = 'K8S resources configuration for notebooks'


class K8SResourcesTensorboards(K8SResourcesOption):
    key = K8S_RESOURCES_TENSORBOARDS
    description = 'K8S resources configuration for tensorboards'
