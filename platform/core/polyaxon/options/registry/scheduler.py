from options import option_namespaces, option_subjects
from options.cache import LONG_CACHE_TTL
from options.option import NAMESPACE_DB_OPTION_MARKER, Option, OptionStores
from options.types import CONF_TYPES

# Global Async Countdown
SCHEDULER_GLOBAL_COUNTDOWN = '{}{}{}'.format(option_namespaces.SCHEDULER,
                                             NAMESPACE_DB_OPTION_MARKER,
                                             option_subjects.GLOBAL_COUNTDOWN)
SCHEDULER_GLOBAL_COUNTDOWN_DELAYED = '{}{}{}'.format(option_namespaces.SCHEDULER,
                                                     NAMESPACE_DB_OPTION_MARKER,
                                                     option_subjects.GLOBAL_COUNTDOWN_DELAYED)
SCHEDULER_RECONCILE_COUNTDOWN = '{}{}{}'.format(option_namespaces.SCHEDULER,
                                                NAMESPACE_DB_OPTION_MARKER,
                                                option_subjects.RECONCILE_COUNTDOWN)


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
    cache_ttl = LONG_CACHE_TTL


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
    cache_ttl = LONG_CACHE_TTL


class SchedulerReconcileCountdown(Option):
    key = SCHEDULER_RECONCILE_COUNTDOWN
    is_global = False
    is_secret = False
    is_optional = True
    is_list = False
    typing = CONF_TYPES.INT
    store = OptionStores.DB_OPTION
    default = 120
    options = None
    description = 'Global count down for reconcile scheduler'
    cache_ttl = LONG_CACHE_TTL
