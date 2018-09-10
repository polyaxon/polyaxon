from polyaxon.config_manager import config

SECRET_KEY = config.get_string('POLYAXON_SECRET_KEY', is_secret=True)
SECRET_INTERNAL_TOKEN = config.get_string('POLYAXON_SECRET_INTERNAL_TOKEN', is_secret=True)
