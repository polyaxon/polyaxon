from options import option_namespaces, option_subjects
from options.cache import FREQUENT_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

K8S_CONFIG_MAPS_BUILD_JOBS = '{}{}{}'.format(option_namespaces.K8S_CONFIG_MAPS,
                                             NAMESPACE_DB_OPTION_MARKER,
                                             option_subjects.BUILD_JOBS)
K8S_CONFIG_MAPS_JOBS = '{}{}{}'.format(option_namespaces.K8S_CONFIG_MAPS,
                                       NAMESPACE_DB_OPTION_MARKER,
                                       option_subjects.JOBS)
K8S_CONFIG_MAPS_EXPERIMENTS = '{}{}{}'.format(option_namespaces.K8S_CONFIG_MAPS,
                                              NAMESPACE_DB_OPTION_MARKER,
                                              option_subjects.EXPERIMENTS)
K8S_CONFIG_MAPS_NOTEBOOKS = '{}{}{}'.format(option_namespaces.K8S_CONFIG_MAPS,
                                            NAMESPACE_DB_OPTION_MARKER,
                                            option_subjects.NOTEBOOKS)
K8S_CONFIG_MAPS_TENSORBOARDS = '{}{}{}'.format(option_namespaces.K8S_CONFIG_MAPS,
                                               NAMESPACE_DB_OPTION_MARKER,
                                               option_subjects.TENSORBOARDS)


class K8SConfigMapsOption(Option):
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    cache_ttl = FREQUENT_CACHE_TTL


class K8SConfigMapsBuildJobs(K8SConfigMapsOption):
    key = K8S_CONFIG_MAPS_BUILD_JOBS
    description = "Config maps to mount for build jobs."


class K8SConfigMapsJobs(K8SConfigMapsOption):
    key = K8S_CONFIG_MAPS_JOBS
    description = "Config maps to mount for jobs."


class K8SConfigMapsExperiments(K8SConfigMapsOption):
    key = K8S_CONFIG_MAPS_EXPERIMENTS
    description = "Config maps to mount for experiments."


class K8SConfigMapsNotebooks(K8SConfigMapsOption):
    key = K8S_CONFIG_MAPS_NOTEBOOKS
    description = "Config maps to mount for notebooks."


class K8SConfigMapsTensorboards(K8SConfigMapsOption):
    key = K8S_CONFIG_MAPS_TENSORBOARDS
    description = "Config maps to mount for tensorboards."
