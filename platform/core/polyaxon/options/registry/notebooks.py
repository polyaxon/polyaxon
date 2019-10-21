from options import option_namespaces, option_subjects
from options.cache import FREQUENT_CACHE_TTL, LONG_CACHE_TTL, MID_FREQUENT_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

NOTEBOOKS_DOCKER_IMAGE = '{}{}{}'.format(option_namespaces.NOTEBOOKS,
                                         NAMESPACE_DB_OPTION_MARKER,
                                         option_subjects.DOCKER_IMAGE)
NOTEBOOKS_BACKEND = '{}{}{}'.format(option_namespaces.NOTEBOOKS,
                                    NAMESPACE_DB_OPTION_MARKER,
                                    option_subjects.BACKEND)
NOTEBOOKS_PORT_RANGE = '{}{}{}'.format(option_namespaces.NOTEBOOKS,
                                       NAMESPACE_DB_OPTION_MARKER,
                                       option_subjects.PORT_RANGE)
NOTEBOOKS_MOUNT_CODE = '{}{}{}'.format(option_namespaces.NOTEBOOKS,
                                       NAMESPACE_DB_OPTION_MARKER,
                                       option_subjects.MOUNT_CODE)


class NotebooksDockerImage(Option):
    key = NOTEBOOKS_DOCKER_IMAGE
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
    description = 'Default docker image to use for running notebooks'
    cache_ttl = FREQUENT_CACHE_TTL


class NotebooksBackend(Option):
    key = NOTEBOOKS_BACKEND
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = 'notebook'
    options = ['notebook', 'lab']
    description = 'The backend to use for running notebooks'
    cache_ttl = MID_FREQUENT_CACHE_TTL


class NotebooksPortRange(Option):
    key = NOTEBOOKS_PORT_RANGE
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = [6700, 7700]
    options = None
    cache_ttl = LONG_CACHE_TTL


class NotebooksMountCode(Option):
    key = NOTEBOOKS_MOUNT_CODE
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.BOOL
    store = OptionStores.DB_OPTION
    default = False
    options = None
    cache_ttl = LONG_CACHE_TTL
