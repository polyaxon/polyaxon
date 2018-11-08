from polyaxon.config_manager import config

ALLOW_USER_PROJECTS = config.get_boolean('POLYAXON_ALLOW_USER_PROJECTS',
                                         is_optional=True,
                                         default=True)
OWNERSHIP_BACKEND = config.get_string('POLYAXON_OWNERSHIP_BACKEND',
                                      is_optional=True)
