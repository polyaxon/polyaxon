from options import option_namespaces, option_subjects
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


class CleaningIntervalsActivityLogs(Option):
    key = CLEANING_INTERVALS_ACTIVITY_LOGS
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 30
    options = None
    description = 'A cleaning interval for activity logs in days'


class CleaningIntervalsNotifications(Option):
    key = CLEANING_INTERVALS_NOTIFICATIONS
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 30
    options = None
    description = 'A cleaning interval for notifications in days'


class CleaningIntervalsArchives(Option):
    key = CLEANING_INTERVALS_ARCHIVES
    is_global = True
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 7
    options = None
    description = 'A cleaning interval for archives in days'
