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


class TTLOption(Option):
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    options = None


class TTLWatchStatuses(TTLOption):
    key = TTL_WATCH_STATUSES
    default = 60 * 20
    description = 'Watch statuses ttl'


class TTLEphemeralToken(TTLOption):
    key = TTL_EPHEMERAL_TOKEN
    default = 60 * 60 * 3
    description = 'Ephemeral token ttl'


class TTLToken(TTLOption):
    key = TTL_TOKEN
    default = 30
    description = 'Token ttl'


class TTLHeartbeat(TTLOption):
    key = TTL_HEARTBEAT
    store = OptionStores.DB_OPTION
    default = 60 * 30
    description = 'Heartbeat ttl'
