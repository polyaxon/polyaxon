from polyaxon.config_manager import config

REGISTRY_IN_CLUSTER = config.get_boolean('POLYAXON_REGISTRY_IN_CLUSTER',
                                         is_optional=True,
                                         default=True)
REGISTRY_LOCALHOST = config.get_string('POLYAXON_REGISTRY_LOCALHOST', is_optional=True)
REGISTRY_HOST = config.get_string('POLYAXON_REGISTRY_HOST', is_optional=True)
