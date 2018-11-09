from polyaxon.config_manager import config

ALLOW_USER_PROJECTS = config.get_boolean('POLYAXON_ALLOW_USER_PROJECTS',
                                         is_optional=True,
                                         default=True)
OWNER_TYPES = config.get_string('POLYAXON_OWNER_TYPES',
                                is_optional=True,
                                is_list=True,
                                default=['user'])
