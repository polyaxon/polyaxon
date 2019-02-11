import json
import os

import rhea

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

K8S_NAMESPACE = config.get_string('POLYAXON_K8S_NAMESPACE')
MOUNT_PATHS_NVIDIA = config.get_dict('POLYAXON_MOUNT_PATHS_NVIDIA', is_optional=True)

CONTAINER_BUILD_STEPS = config.get_string('POLYAXON_CONTAINER_BUILD_STEPS', is_optional=True)
if CONTAINER_BUILD_STEPS:
    CONTAINER_BUILD_STEPS = json.loads(CONTAINER_BUILD_STEPS)

CONTAINER_ENV_VARS = config.get_string('POLYAXON_CONTAINER_ENV_VARS', is_optional=True)
if CONTAINER_ENV_VARS:
    CONTAINER_ENV_VARS = json.loads(CONTAINER_ENV_VARS)
