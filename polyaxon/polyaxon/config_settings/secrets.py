from polyaxon.config_manager import config

SECRET_KEY = config.get_string('POLYAXON_SECRET_KEY', is_secret=True)
INTERNAL_SECRET_TOKEN = config.get_string('POLYAXON_INTERNAL_SECRET_TOKEN', is_secret=True)
