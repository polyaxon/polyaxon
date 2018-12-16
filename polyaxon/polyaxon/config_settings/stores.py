from polyaxon.config_manager import config

STORES_BACKEND = config.get_string('POLYAXON_ACCESS_STORES', is_optional=True)
