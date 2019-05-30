from constants.pull_policies import PullPolicies
from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

SIDECARS_DOCKER_IMAGE = '{}{}{}'.format(option_namespaces.SIDECARS,
                                        NAMESPACE_DB_OPTION_MARKER,
                                        option_subjects.DOCKER_IMAGE)
SIDECARS_IMAGE_PULL_POLICY = '{}{}{}'.format(option_namespaces.SIDECARS,
                                             NAMESPACE_DB_OPTION_MARKER,
                                             option_subjects.IMAGE_PULL_POLICY)
SIDECARS_SLEEP_INTERVAL = '{}{}{}'.format(option_namespaces.SIDECARS,
                                          NAMESPACE_DB_OPTION_MARKER,
                                          option_subjects.SLEEP_INTERVAL)


class SidecarsDockerImage(Option):
    key = SIDECARS_DOCKER_IMAGE
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = 'polyaxon/polyaxon-sidecar:0.0.4'
    options = None
    description = 'Sidecar docker image'


class SidecarsImagePullPolicy(Option):
    key = SIDECARS_IMAGE_PULL_POLICY
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = PullPolicies.ALWAYS
    options = PullPolicies.VALUES
    description = 'The sidecar container pull policy'


class SidecarsSleepInterval(Option):
    key = SIDECARS_SLEEP_INTERVAL
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = 1
    options = None
    description = 'Sleep interval'
