from constants.pull_policies import PullPolicies
from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

INIT_DOCKER_IMAGE = '{}{}{}'.format(option_namespaces.INIT,
                                    NAMESPACE_DB_OPTION_MARKER,
                                    option_subjects.DOCKER_IMAGE)
INIT_IMAGE_PULL_POLICY = '{}{}{}'.format(option_namespaces.INIT,
                                         NAMESPACE_DB_OPTION_MARKER,
                                         option_subjects.IMAGE_PULL_POLICY)


class InitDockerImage(Option):
    key = INIT_DOCKER_IMAGE
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = 'polyaxon/polyaxon-init:0.5.0rc2'
    options = None
    description = 'The docker image to use for init container'


class InitImagePullPolicy(Option):
    key = INIT_IMAGE_PULL_POLICY
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = PullPolicies.ALWAYS
    options = PullPolicies.VALUES
    description = 'The init container pull policy'
