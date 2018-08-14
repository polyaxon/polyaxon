import os

from distutils.util import strtobool  # pylint:disable=import-error

from unipath import Path

from config_manager.config_manager import ConfigManager


def base_directory():
    return Path(__file__).ancestor(3)


ROOT_DIR = base_directory()
DATA_DIR = ROOT_DIR.child('data')
ENV_VARS_DIR = ROOT_DIR.child('polyaxon').child('polyaxon').child('env_vars')
TESTING = bool(strtobool(os.getenv('TESTING', "0")))


config_values = [
    '{}/defaults.json'.format(ENV_VARS_DIR),
    os.environ,
]

if TESTING:
    config_values.append('{}/test.json'.format(ENV_VARS_DIR))
elif os.path.isfile('{}/local.json'.format(ENV_VARS_DIR)):
    config_values.append('{}/local.json'.format(ENV_VARS_DIR))

config = ConfigManager.read_configs(config_values)
