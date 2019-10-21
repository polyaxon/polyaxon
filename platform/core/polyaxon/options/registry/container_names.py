from options import option_namespaces, option_subjects
from options.cache import LONG_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

CONTAINER_NAME_BUILD_JOBS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                            NAMESPACE_DB_OPTION_MARKER,
                                            option_subjects.BUILD_JOBS)
CONTAINER_NAME_EXPERIMENT_JOBS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                                 NAMESPACE_DB_OPTION_MARKER,
                                                 option_subjects.EXPERIMENT_JOBS)

CONTAINER_NAME_JOBS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                      NAMESPACE_DB_OPTION_MARKER,
                                      option_subjects.JOBS)

CONTAINER_NAME_TF_JOBS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                         NAMESPACE_DB_OPTION_MARKER,
                                         option_subjects.TF_JOBS)

CONTAINER_NAME_PYTORCH_JOBS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                              NAMESPACE_DB_OPTION_MARKER,
                                              option_subjects.PYTORCH_JOBS)

CONTAINER_NAME_SIDECARS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                          NAMESPACE_DB_OPTION_MARKER,
                                          option_subjects.SIDECARS)

CONTAINER_NAME_INIT = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                      NAMESPACE_DB_OPTION_MARKER,
                                      option_subjects.INIT)

CONTAINER_NAME_PLUGIN_JOBS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                             NAMESPACE_DB_OPTION_MARKER,
                                             option_subjects.PLUGIN_JOBS)


class ContainerNameOption(Option):
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    options = None
    cache_ttl = LONG_CACHE_TTL


class ContainerNameBuildJobs(ContainerNameOption):
    key = CONTAINER_NAME_BUILD_JOBS
    default = 'polyaxon-dockerizer-job'


class ContainerNameExperimentJobs(ContainerNameOption):
    key = CONTAINER_NAME_EXPERIMENT_JOBS
    default = 'polyaxon-experiment-job'


class ContainerNameJobs(ContainerNameOption):
    key = CONTAINER_NAME_JOBS
    default = 'polyaxon-job'


class ContainerNameTFJobs(ContainerNameOption):
    key = CONTAINER_NAME_TF_JOBS
    default = 'tensorflow'


class ContainerNamePytorchJobs(ContainerNameOption):
    key = CONTAINER_NAME_PYTORCH_JOBS
    default = 'pytorch'


class ContainerNameSidecars(ContainerNameOption):
    key = CONTAINER_NAME_SIDECARS
    default = 'polyaxon-sidecar-job'


class ContainerNameInit(ContainerNameOption):
    key = CONTAINER_NAME_INIT
    default = 'polyaxon-init-job'


class ContainerNamePluginJobs(ContainerNameOption):
    key = CONTAINER_NAME_PLUGIN_JOBS
    default = 'polyaxon-plugin-job'
