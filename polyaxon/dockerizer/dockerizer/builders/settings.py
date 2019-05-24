import json
import os

import rhea

from rhea import RheaError, rhea_parser
from rhea.specs import UriSpec
from unipath import Path


def base_directory():
    return Path(__file__).ancestor(3)


ROOT_DIR = base_directory()
ENV_VARS_DIR = ROOT_DIR.child('env_vars')

config_values = [
    '{}/default.json'.format(ENV_VARS_DIR),
    os.environ,
]

if os.path.isfile('{}/local.json'.format(ENV_VARS_DIR)):
    config_values.append('{}/local.json'.format(ENV_VARS_DIR))

config = rhea.Rhea.read_configs(config_values)

REGISTRY_USER = config.get_string('POLYAXON_REGISTRY_USER',
                                  is_optional=True)
REGISTRY_PASSWORD = config.get_string('POLYAXON_REGISTRY_PASSWORD',
                                      is_secret=True,
                                      is_optional=True)
REGISTRY_URI = config.get_string('POLYAXON_REGISTRY_URI',
                                 is_optional=True)

INTERNAL_REGISTRY = None
if all([REGISTRY_USER, REGISTRY_PASSWORD, REGISTRY_URI]):
    INTERNAL_REGISTRY = UriSpec(REGISTRY_USER, REGISTRY_PASSWORD, REGISTRY_URI)

# This is duplicated
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

            registry_spec = rhea_parser.parse_uri_spec(registry_spec)

        if registry_spec:
            registries.append(registry_spec)

    return registries


PRIVATE_REGISTRIES = get_external_registries()
