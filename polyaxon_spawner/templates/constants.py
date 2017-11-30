# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.polyaxonfile import constants

ENV_VAR_TEMPLATE = '{name: "{var_name}", value: "{var_value}"}'
VOLUME_NAME = 'pv-{vol_name}'
VOLUME_CLAIM_NAME = 'pvc-{vol_name}'
CONFIG_MAP_NAME = '{project}-xp{experiment}-{role}'
CONFIG_MAP_LABELS = ()
CONFIG_MAP_KEY_NAME = 'CM_{project}_xp{experiment}_{role}_{task_type}'
POD_CONTAINER_PROJECT_NAME = '{project}-{name}'
DEPLOYMENT_NAME = '{project}-{name}'
CLUSTER_SECRET = 'polyaxon-cluster-secret'

JOB_DOCKER_NAME = 'polyaxon/polyaxon-lib:0.0.1'
SIDECAR_DOCKER_IMAGE = 'polyaxon/polyaxon-api:0.0.1'


def SIDECAR_ARGS_FN(container_job_name, pod_id):
    return ["python3", "api/manage.py", "monitor_resources", container_job_name, pod_id,
            "--log_sleep_interval={{ .Values.events.namespace.amqpReconnectInterval | quote }}",
            "--persist={{ .Values.events.namespace.amqpReconnectInterval | quote }}"]


ROLE_LABELS_WORKER = 'polyaxon-workers'
TYPE_LABELS_EXPERIMENT = 'polyaxon-experiment'
JOB_CONTAINER_NAME = 'experiment-job'
SIDECAR_CONTAINER_NAME = 'experiment-job-sidecar'

DATA_VOLUME = constants.DATA_VOLUME
LOGS_VOLUME = constants.LOGS_VOLUME
POLYAXON_FILES_VOLUME = constants.POLYAXON_FILES_VOLUME
TASK_NAME = constants.TASK_NAME
DEFAULT_PORT = constants.DEFAULT_PORT
