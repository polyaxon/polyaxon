import json

from rhea import RheaError
from rhea.manager import UriSpec

from polyaxon.config_manager import config

REGISTRY_USER = config.get_string('POLYAXON_REGISTRY_USER', is_optional=True)
REGISTRY_PASSWORD = config.get_string('POLYAXON_REGISTRY_PASSWORD', is_optional=True)
REGISTRY_PORT = config.get_string('POLYAXON_REGISTRY_PORT', is_optional=True)
REGISTRY_NODE_PORT = config.get_string('POLYAXON_REGISTRY_NODE_PORT', is_optional=True)
REGISTRY_HOST = config.get_string('POLYAXON_REGISTRY_HOST', is_optional=True)
REGISTRY_IN_CLUSTER = config.get_boolean('POLYAXON_REGISTRY_IN_CLUSTER',
                                         is_optional=True,
                                         default=True)
REGISTRY_LOCAL_URI = '{}:{}'.format('127.0.0.1', REGISTRY_NODE_PORT)

REGISTRY_URI = None
if REGISTRY_HOST:
    if REGISTRY_PORT:
        REGISTRY_URI = '{}:{}'.format(REGISTRY_HOST, REGISTRY_PORT)
    else:
        REGISTRY_URI = REGISTRY_HOST
if not REGISTRY_URI:
    REGISTRY_URI = REGISTRY_LOCAL_URI
PRIVATE_REGISTRIES_PREFIX = 'POLYAXON_PRIVATE_REGISTRY_'


def get_external_registries():
    registries = []
    for key in config.keys_startswith(PRIVATE_REGISTRIES_PREFIX):

        try:
            registry_dict = config.get_dict(key, is_secret=True)
            registry_spec = UriSpec(**registry_dict)
        except RheaError:
            registry_spec = config.get_string(key, is_secret=True)
            try:
                # We might get this value from a chart with `toJson` applied.
                registry_spec = json.loads(registry_spec)
            except json.decoder.JSONDecodeError:
                pass

            registry_spec = config.parse_uri_spec(registry_spec)

        if registry_spec:
            registries.append(registry_spec)

    return registries


PRIVATE_REGISTRIES = get_external_registries()
