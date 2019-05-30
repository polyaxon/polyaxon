from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

TENSORBOARDS_DOCKER_IMAGE = '{}{}{}'.format(option_namespaces.TENSORBOARDS,
                                            NAMESPACE_DB_OPTION_MARKER,
                                            option_subjects.DOCKER_IMAGE)
TENSORBOARDS_PORT_RANGE = '{}{}{}'.format(option_namespaces.TENSORBOARDS,
                                          NAMESPACE_DB_OPTION_MARKER,
                                          option_subjects.PORT_RANGE)


class TensorboardsDockerImage(Option):
    key = TENSORBOARDS_DOCKER_IMAGE
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = 'tensorflow/tensorflow:1.11.0-py3'
    options = None
    description = 'Default docker image to use for running tensorboards'


class TensorboardsPortRange(Option):
    key = TENSORBOARDS_PORT_RANGE
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = [5700, 6700]
    options = None
