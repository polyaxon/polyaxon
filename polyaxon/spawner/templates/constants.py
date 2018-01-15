# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings

JOB_NAME = 'plxjob-{task_type}{task_idx}-{experiment_uuid}'
DEFAULT_PORT = 2222
ENV_VAR_TEMPLATE = '{name: "{var_name}", value: "{var_value}"}'
VOLUME_CLAIM_NAME = 'polyaxon-pvc-{vol_name}'
CONFIG_MAP_NAME = 'plx-config-{experiment_uuid}'
SECRET_NAME = 'plx-secret-{experiment_uuid}'
CONFIG_MAP_CLUSTER_KEY_NAME = 'POLYAXON_CLUSTER'
CONFIG_MAP_DECLARATIONS_KEY_NAME = 'POLYAXON_DECLARATIONS'
CONFIG_MAP_EXPERIMENT_INFO_KEY_NAME = 'POLYAXON_EXPERIMENT_INFO'
CONFIG_MAP_TASK_INFO_KEY_NAME = 'POLYAXON_TASK_INFO'
CONFIG_MAP_LOG_LEVEL_KEY_NAME = 'POLYAXON_LOG_LEVEL'
CONFIG_MAP_EXPERIMENT_OUTPUTS_PATH_KEY_NAME = 'POLYAXON_OUTPUTS_PATH'
CONFIG_MAP_API_KEY_NAME = 'POLYAXON_API'
SECRET_USER_TOKEN = 'POLYAXON_USER_TOKEN'
POD_CONTAINER_PROJECT_NAME = 'plxproject-{project_uuid}-{name}'
DEPLOYMENT_NAME = 'plxproject-{project_uuid}-{name}'


def SIDECAR_ARGS_FN(pod_id):
    return [pod_id,
            "--log_sleep_interval={}".format(settings.JOB_SIDECAR_LOG_SLEEP_INTERVAL),
            "--persist={}".format(settings.JOB_SIDECAR_PERSIST)]


DATA_VOLUME = 'data'
OUTPUTS_VOLUME = 'outputs'
