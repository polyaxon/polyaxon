from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

TTL_WATCH_STATUSES = '{}{}{}'.format(option_namespaces.TTL,
                                     NAMESPACE_DB_OPTION_MARKER,
                                     option_subjects.WATCH_STATUSES)

TTL_EPHEMERAL_TOKEN = '{}{}{}'.format(option_namespaces.TTL,
                                      NAMESPACE_DB_OPTION_MARKER,
                                      option_subjects.EPHEMERAL_TOKEN)

# Heartbeat timeout (status -> failed as zombie)
TTL_HEARTBEAT = '{}{}{}'.format(option_namespaces.TTL,
                                NAMESPACE_DB_OPTION_MARKER,
                                option_subjects.HEARTBEAT)

# Token time in days
TTL_TOKEN = '{}{}{}'.format(option_namespaces.TTL,
                            NAMESPACE_DB_OPTION_MARKER,
                            option_subjects.TOKEN)


class TTLWatchStatuses(Option):
    key = TTL_WATCH_STATUSES
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 60 * 20
    options = None
    description = 'Watch statuses ttl'


class TTLEphemeralToken(Option):
    key = TTL_EPHEMERAL_TOKEN
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 60 * 60 * 3
    options = None
    description = 'Ephemeral token ttl'


class TTLToken(Option):
    key = TTL_TOKEN
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 30
    options = None
    description = 'Token ttl'


class TTLHeartbeat(Option):
    key = TTL_HEARTBEAT
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 60 * 30
    options = None
    description = 'Heartbeat ttl'
