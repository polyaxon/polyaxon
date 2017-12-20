# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from django.conf import settings

JOB_NAME = 'plxjob-{task_type}{task_idx}-{experiment_uuid}'
DEFAULT_PORT = 2222
ENV_VAR_TEMPLATE = '{name: "{var_name}", value: "{var_value}"}'
VOLUME_NAME = 'pv-{vol_name}'
VOLUME_CLAIM_NAME = 'pvc-{vol_name}'
CLUSTER_CONFIG_MAP_NAME = 'plxcluster-{experiment_uuid}'
CLUSTER_CONFIG_MAP_KEY_NAME = 'plxcluster_{experiment_uuid}_{task_type}'
POD_CONTAINER_PROJECT_NAME = 'plxproject-{project_uuid}-{name}'
DEPLOYMENT_NAME = 'plxproject-{project_uuid}-{name}'


def SIDECAR_ARGS_FN(pod_id):
    return ["python3", "api/manage.py", "start_sidecar", pod_id,
            "--log_sleep_interval={}".format(settings.JOB_SIDECAR_LOG_SLEEP_INTERVAL),
            "--persist={}".format(settings.JOB_SIDECAR_PERSIST)]


DATA_VOLUME = 'data'
OUTPUTS_VOLUME = 'outputs'
