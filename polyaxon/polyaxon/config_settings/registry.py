from polyaxon.config_manager import config

REGISTRY_USER = config.get_string('POLYAXON_REGISTRY_USER', is_optional=True)
REGISTRY_PASSWORD = config.get_string('POLYAXON_REGISTRY_PASSWORD', is_optional=True)
REGISTRY_HOST_NAME = config.get_string('POLYAXON_REGISTRY_HOST', is_optional=True)
REGISTRY_PORT = config.get_string('POLYAXON_REGISTRY_PORT', is_optional=True)
REGISTRY_NODE_PORT = config.get_string('POLYAXON_REGISTRY_NODE_PORT', is_optional=True)
REGISTRY_HOST = '{}:{}'.format('127.0.0.1', REGISTRY_NODE_PORT)
PRIVATE_REGISTRIES_PREFIX = 'POLYAXON_PRIVATE_REGISTRY_'


def get_external_registries():
    registries = []
    for key in config.params_startswith(PRIVATE_REGISTRIES_PREFIX):
        registry_spec = config.get_string(key, is_secret=True)
        registry_spec = config.parse_uri_spec(registry_spec)
        if registry_spec:
            registries.append(registry_spec)

    return registries


PRIVATE_REGISTRIES = get_external_registries()
