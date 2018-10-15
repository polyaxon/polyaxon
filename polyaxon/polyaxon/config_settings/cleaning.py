from polyaxon.config_manager import config


class CleaningIntervals(object):
    ACTIVITY_LOGS = config.get_int(
        'POLYAXON_CLEANING_INTERVALS_ACTIVITY_LOGS',
        is_optional=True,
        default=60)
    NOTIFICATIONS = config.get_int(
        'POLYAXON_CLEANING_INTERVALS_NOTIFICATIONS',
        is_optional=True,
        default=30)
