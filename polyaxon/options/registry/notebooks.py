from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_MARKER, Option, OptionStores
from options.types import CONF_TYPES

NOTEBOOKS_DOCKER_IMAGE = '{}{}{}'.format(option_namespaces.NOTEBOOKS,
                                         NAMESPACE_DB_MARKER,
                                         option_subjects.DOCKER_IMAGE)
NOTEBOOKS_BACKEND = '{}{}{}'.format(option_namespaces.NOTEBOOKS,
                                    NAMESPACE_DB_MARKER,
                                    option_subjects.BACKEND)
NOTEBOOKS_PORT_RANGE = '{}{}{}'.format(option_namespaces.NOTEBOOKS,
                                       NAMESPACE_DB_MARKER,
                                       option_subjects.PORT_RANGE)
NOTEBOOKS_MOUNT_CODE = '{}{}{}'.format(option_namespaces.NOTEBOOKS,
                                       NAMESPACE_DB_MARKER,
                                       option_subjects.MOUNT_CODE)


class NotebooksDockerImage(Option):
    key = NOTEBOOKS_DOCKER_IMAGE
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB
    default = None
    options = None
    description = 'Default docker image to use for running notebooks'


class NotebooksBackend(Option):
    key = NOTEBOOKS_BACKEND
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB
    default = 'notebook'
    options = None
    description = 'The backend to use for running notebooks'


class NotebooksPortRange(Option):
    key = NOTEBOOKS_PORT_RANGE
    is_global = False
    is_secret = False
    is_optional = True
    is_list = True
    typing = CONF_TYPES.INT
    store = OptionStores.DB
    default = [6700, 7700]
    options = None


class NotebooksMountCode(Option):
    key = NOTEBOOKS_MOUNT_CODE
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.BOOL
    store = OptionStores.DB
    default = False
    options = None
