from polyaxon.config_manager import config

API_HOST = config.get_string('POLYAXON_API_HOST', is_optional=True)
