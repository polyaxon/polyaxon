# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon_schemas.polyaxonfile import constants

DOCKER_IMAGE = 'polyaxon/polyaxon:lib-cpu-3-121'
ENV_VAR_TEMPLATE = '{name: "{var_name}", value: "{var_value}"}'
VOLUME_NAME = 'pv-{project}-{vol_name}'
VOLUME_CLAIM_NAME = 'pvc-{project}-{vol_name}'
GPU_RESOURCES = '{alpha.kubernetes.io/nvidia-gpu: {}'
CONFIG_MAP_CLUSTER_NAME = '{project}-xp{experiment}-cluster'
CONFIG_MAP_CLUSTER_KEY_NAME = 'CM_{project}_xp{experiment}_cluster_{task_type}'
TASK_LABELS = ('project: "{project}", '
               'experiment: "{experiment}", '
               'task_type: "{task_type}", '
               'task_id: "{task_id}", '
               'task: "{task_name}"')
POD_CONTAINER_TASK_NAME = '{project}-xp{experiment}-{task_type}{task_id}'
POD_CONTAINER_PROJECT_NAME = '{project}-{name}'
DEPLOYMENT_NAME = '{project}-{name}'


DATA_VOLUME = constants.DATA_VOLUME
LOGS_VOLUME = constants.LOGS_VOLUME
POLYAXON_FILES_VOLUME = constants.POLYAXON_FILES_VOLUME
TASK_NAME = constants.TASK_NAME
DEFAULT_PORT = constants.DEFAULT_PORT
