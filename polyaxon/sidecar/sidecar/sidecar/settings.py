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
CONTAINER_NAME_EXPERIMENT_JOB = config.get_string('POLYAXON_CONTAINER_NAME_EXPERIMENT_JOB',
                                                  is_optional=True,
                                                  default='polyaxon-experiment-job')
CONTAINER_NAME_JOB = config.get_string('POLYAXON_CONTAINER_NAME_JOB',
                                       is_optional=True,
                                       default='polyaxon-job')
# Labels
APP_LABELS_TENSORBOARD = config.get_string('POLYAXON_APP_LABELS_TENSORBOARD',
                                           is_optional=True,
                                           default='polyaxon-tensorboard')
APP_LABELS_NOTEBOOK = config.get_string('POLYAXON_APP_LABELS_NOTEBOOK',
                                        is_optional=True,
                                        default='polyaxon-notebook')
APP_LABELS_DOCKERIZER = config.get_string('POLYAXON_APP_LABELS_DOCKERIZER',
                                          is_optional=True,
                                          default='polyaxon-dockerizer')
APP_LABELS_EXPERIMENT = config.get_string('POLYAXON_APP_LABELS_EXPERIMENT',
                                          is_optional=True,
                                          default='polyaxon-experiment')
APP_LABELS_JOB = config.get_string('POLYAXON_APP_LABELS_JOB',
                                   is_optional=True,
                                   default='polyaxon-job')

MESSAGES_COUNT = config.get_string('POLYAXON_MESSAGES_COUNT',
                                   is_optional=True,
                                   default=50)
MESSAGES_TIMEOUT = config.get_string('POLYAXON_MESSAGES_TIMEOUT',
                                     is_optional=True,
                                     default=5)
MESSAGES_TIMEOUT_SHORT = config.get_string('POLYAXON_MESSAGES_TIMEOUT_SHORT',
                                           is_optional=True,
                                           default=2)
CHECK_ALIVE_INTERVAL = config.get_string('POLYAXON_CHECK_ALIVE_INTERVAL',
                                         is_optional=True,
                                         default=10)
