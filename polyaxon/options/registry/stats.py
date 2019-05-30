from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

STATS_DEFAULT_PREFIX = '{}{}{}'.format(option_namespaces.STATS,
                                       NAMESPACE_DB_OPTION_MARKER,
                                       option_subjects.DEFAULT_PREFIX)


class StatsDefaultPrefix(Option):
    key = STATS_DEFAULT_PREFIX
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.STR
    store = OptionStores.DB_OPTION
    default = None
    options = None
