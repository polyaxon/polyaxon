from options import option_namespaces, option_subjects
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

# Global Async Countdown
SCHEDULER_GLOBAL_COUNTDOWN = '{}{}{}'.format(option_namespaces.SCHEDULER,
                                             NAMESPACE_DB_OPTION_MARKER,
                                             option_subjects.GLOBAL_COUNTDOWN)
SCHEDULER_GLOBAL_COUNTDOWN_DELAYED = '{}{}{}'.format(option_namespaces.SCHEDULER,
                                                     NAMESPACE_DB_OPTION_MARKER,
                                                     option_subjects.GLOBAL_COUNTDOWN_DELAYED)


class SchedulerCountdown(Option):
    key = SCHEDULER_GLOBAL_COUNTDOWN
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 1
    options = None
    description = 'Global count down for scheduler'


class SchedulerCountdownDelayed(Option):
    key = SCHEDULER_GLOBAL_COUNTDOWN_DELAYED
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 3
    options = None
    description = 'Global delayed count down for scheduler'
