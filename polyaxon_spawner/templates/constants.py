# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.polyaxonfile import constants

DOCKER_JOB_IMAGE = 'polyaxon/polyaxon-lib:0.0.1'
DOCKER_SIDECAR_IMAGE = 'polyaxon/polyaxon-events:0.0.1'
SIDECAR_CMD = 'python3 polyaxon_events/events/sidecar.py'
ENV_VAR_TEMPLATE = '{name: "{var_name}", value: "{var_value}"}'
VOLUME_NAME = 'pv-{vol_name}'
VOLUME_CLAIM_NAME = 'pvc-{vol_name}'
CONFIG_MAP_NAME = '{project}-xp{experiment}-{role}'
CONFIG_MAP_LABELS = ()
CONFIG_MAP_KEY_NAME = 'CM_{project}_xp{experiment}_{role}_{task_type}'
POD_CONTAINER_PROJECT_NAME = '{project}-{name}'
DEPLOYMENT_NAME = '{project}-{name}'
CLUSTER_SECRET = 'polyaxon-cluster-secret'

WORKER_ROLE_LABEL = 'polyaxon-workers'
EXPERIMENT_TYPE_LABEL = 'polyaxon-experiment'
POD_CONTAINER_JOB_NAME = 'experiment-job'
POD_CONTAINER_SIDECAR_NAME = 'experiment-job-sidecar'


DATA_VOLUME = constants.DATA_VOLUME
LOGS_VOLUME = constants.LOGS_VOLUME
POLYAXON_FILES_VOLUME = constants.POLYAXON_FILES_VOLUME
TASK_NAME = constants.TASK_NAME
DEFAULT_PORT = constants.DEFAULT_PORT
