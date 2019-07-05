from constants.backends import NATIVE_BACKEND
from constants.pull_policies import PullPolicies
from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

BUILD_JOBS_BACKEND = '{}{}{}'.format(option_namespaces.BUILD_JOBS,
                                     NAMESPACE_DB_OPTION_MARKER,
                                     option_subjects.BACKEND)
BUILD_JOBS_ALWAYS_PULL_LATEST = '{}{}{}'.format(option_namespaces.BUILD_JOBS,
                                                NAMESPACE_DB_OPTION_MARKER,
                                                option_subjects.ALWAYS_PULL_LATEST)
BUILD_JOBS_LANG_ENV = '{}{}{}'.format(option_namespaces.BUILD_JOBS,
                                      NAMESPACE_DB_OPTION_MARKER,
                                      option_subjects.LANG_ENV)
BUILD_JOBS_DOCKER_IMAGE = '{}{}{}'.format(option_namespaces.BUILD_JOBS,
                                          NAMESPACE_DB_OPTION_MARKER,
                                          option_subjects.DOCKER_IMAGE)
BUILD_JOBS_IMAGE_PULL_POLICY = '{}{}{}'.format(option_namespaces.BUILD_JOBS,
                                               NAMESPACE_DB_OPTION_MARKER,
                                               option_subjects.IMAGE_PULL_POLICY)
BUILD_JOBS_SET_SECURITY_CONTEXT = '{}{}{}'.format(option_namespaces.BUILD_JOBS,
                                                  NAMESPACE_DB_OPTION_MARKER,
                                                  option_subjects.SET_SECURITY_CONTEXT)
KANIKO_DOCKER_IMAGE = '{}{}{}'.format(option_namespaces.KANIKO,
                                      NAMESPACE_DB_OPTION_MARKER,
                                      option_subjects.DOCKER_IMAGE)
KANIKO_IMAGE_PULL_POLICY = '{}{}{}'.format(option_namespaces.KANIKO,
                                           NAMESPACE_DB_OPTION_MARKER,
                                           option_subjects.IMAGE_PULL_POLICY)


class BuildJobsBackend(Option):
    key = BUILD_JOBS_BACKEND
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = NATIVE_BACKEND
    options = None
    description = 'The backend to use for building container images'


class BuildJobsAlwaysPullLatest(Option):
    key = BUILD_JOBS_ALWAYS_PULL_LATEST
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.BOOL
    store = OptionStores.DB_OPTION
    default = False
    options = None
    description = 'Whether to always pull image tagged with latest tag'


class BuildJobsLangEnv(Option):
    key = BUILD_JOBS_LANG_ENV
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'To add language environment vars for the provided language on the docker image'


class BuildJobsDockerImage(Option):
    key = BUILD_JOBS_DOCKER_IMAGE
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = 'polyaxon/polyaxon-dockerizer:0.5.0'
    options = None
    description = 'The dockerizer docker image'


class BuildJobsImagePullPolicy(Option):
    key = BUILD_JOBS_IMAGE_PULL_POLICY
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = PullPolicies.ALWAYS
    options = PullPolicies.VALUES
    description = 'The dockerizer pull policy'


class BuildJobsSetSecurityContext(Option):
    key = BUILD_JOBS_SET_SECURITY_CONTEXT
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.BOOL
    store = OptionStores.DB_OPTION
    default = True
    options = None
    description = 'Whether to set user/group on the image to not run containers as root'


class KanikoDockerImage(Option):
    key = KANIKO_DOCKER_IMAGE
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = 'gcr.io/kaniko-project/executor:v0.7.0'
    options = None
    description = 'Kaniko docker image to use'


class KanikoImagePullPolicy(Option):
    key = KANIKO_IMAGE_PULL_POLICY
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = PullPolicies.IF_NOT_PRESENT
    options = PullPolicies.VALUES
    description = 'Kaniko pull policy'
