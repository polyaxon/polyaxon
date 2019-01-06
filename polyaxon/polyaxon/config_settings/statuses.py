from polyaxon.config_manager import config

TTL_WATCH_STATUSES = config.get_int('POLYAXON_TTL_WATCH_STATUSES',
                                    is_optional=True,
                                    default=60 * 20)
