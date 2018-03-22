from polyaxon.utils import config

SECRET_KEY = config.get_string('POLYAXON_SECRET_KEY', is_secret=True)
