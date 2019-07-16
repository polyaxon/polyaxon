from options import option_namespaces, option_subjects
from options.cache import LONG_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

CLEANING_INTERVALS_ACTIVITY_LOGS = '{}{}{}'.format(option_namespaces.CLEANING_INTERVALS,
                                                   NAMESPACE_DB_OPTION_MARKER,
                                                   option_subjects.ACTIVITY_LOGS)

CLEANING_INTERVALS_NOTIFICATIONS = '{}{}{}'.format(option_namespaces.CLEANING_INTERVALS,
                                                   NAMESPACE_DB_OPTION_MARKER,
                                                   option_subjects.NOTIFICATIONS)
CLEANING_INTERVALS_ARCHIVES = '{}{}{}'.format(option_namespaces.CLEANING_INTERVALS,
                                              NAMESPACE_DB_OPTION_MARKER,
                                              option_subjects.ARCHIVES)


class CleaningIntervalsOption(Option):
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    options = None
    cache_ttl = LONG_CACHE_TTL


class CleaningIntervalsActivityLogs(CleaningIntervalsOption):
    key = CLEANING_INTERVALS_ACTIVITY_LOGS
    default = 30
    description = 'A cleaning interval for activity logs in days'


class CleaningIntervalsNotifications(CleaningIntervalsOption):
    key = CLEANING_INTERVALS_NOTIFICATIONS
    default = 30
    description = 'A cleaning interval for notifications in days'


class CleaningIntervalsArchives(CleaningIntervalsOption):
    key = CLEANING_INTERVALS_ARCHIVES
    store = OptionStores.DB_OPTION
    default = 7
    description = 'A cleaning interval for archives in days'
