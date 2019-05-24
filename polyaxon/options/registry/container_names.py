from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_MARKER, Option, OptionStores
from options.types import CONF_TYPES

CONTAINER_NAME_BUILD_JOBS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                            NAMESPACE_DB_MARKER,
                                            option_subjects.BUILD_JOBS)
CONTAINER_NAME_EXPERIMENT_JOBS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                                 NAMESPACE_DB_MARKER,
                                                 option_subjects.EXPERIMENT_JOBS)

CONTAINER_NAME_JOBS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                      NAMESPACE_DB_MARKER,
                                      option_subjects.JOBS)

CONTAINER_NAME_TF_JOBS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                         NAMESPACE_DB_MARKER,
                                         option_subjects.TF_JOBS)

CONTAINER_NAME_PYTORCH_JOBS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                              NAMESPACE_DB_MARKER,
                                              option_subjects.PYTORCH_JOBS)

CONTAINER_NAME_SIDECARS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                          NAMESPACE_DB_MARKER,
                                          option_subjects.SIDECARS)

CONTAINER_NAME_INIT = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                      NAMESPACE_DB_MARKER,
                                      option_subjects.INIT)

CONTAINER_NAME_PLUGIN_JOBS = '{}{}{}'.format(option_namespaces.CONTAINER_NAME,
                                             NAMESPACE_DB_MARKER,
                                             option_subjects.PLUGIN_JOBS)


class ContainerNameBuildJobs(Option):
    key = CONTAINER_NAME_BUILD_JOBS
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB
    default = 'polyaxon-dockerizer-job'
    options = None


class ContainerNameExperimentJobs(Option):
    key = CONTAINER_NAME_EXPERIMENT_JOBS
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB
    default = 'polyaxon-experiment-job'
    options = None


class ContainerNameJobs(Option):
    key = CONTAINER_NAME_JOBS
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB
    default = 'polyaxon-job'
    options = None


class ContainerNameTFJobs(Option):
    key = CONTAINER_NAME_TF_JOBS
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB
    default = 'tensorflow'
    options = None


class ContainerNamePytorchJobs(Option):
    key = CONTAINER_NAME_PYTORCH_JOBS
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB
    default = 'pytorch'
    options = None


class ContainerNameSidecars(Option):
    key = CONTAINER_NAME_SIDECARS
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB
    default = 'polyaxon-sidecar-job'
    options = None


class ContainerNameInit(Option):
    key = CONTAINER_NAME_INIT
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB
    default = 'polyaxon-init-job'
    options = None


class ContainerNamePluginJobs(Option):
    key = CONTAINER_NAME_PLUGIN_JOBS
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB
    default = 'polyaxon-plugin-job'
    options = None
