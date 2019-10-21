from polyaxon.config_manager import config

CI_BACKEND = config.get_string('POLYAXON_CI_BACKEND', is_optional=True)
