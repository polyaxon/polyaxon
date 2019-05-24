from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_MARKER, Option, OptionStores
from options.types import CONF_TYPES

GROUPS_CHECK_INTERVAL = '{}{}{}'.format(option_namespaces.GROUPS,
                                        NAMESPACE_DB_MARKER,
                                        option_subjects.CHECK_INTERVAL)

GROUPS_CHUNKS = '{}{}{}'.format(option_namespaces.GROUPS,
                                NAMESPACE_DB_MARKER,
                                option_subjects.CHUNKS)


class GroupsCheckInterval(Option):
    key = GROUPS_CHECK_INTERVAL
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB
    default = 5
    options = None
    description = 'Interval to reconcile experiment groups'


class GroupsChunks(Option):
    key = GROUPS_CHUNKS
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB
    default = 50
    options = None
    description = ('A variable to optimize the chunk of objects created '
                   'at a time by the experiment groups')
