# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from api.utils import config

ROLE_LABELS_WORKER = config.get_string('POLYAXON_ROLE_LABELS_WORKER')
TYPE_LABELS_EXPERIMENT = config.get_string('POLYAXON_TYPE_LABELS_EXPERIMENT')
JOB_CONTAINER_NAME = config.get_string('POLYAXON_JOB_CONTAINER_NAME')
JOB_SIDECAR_CONTAINER_NAME = config.get_string('POLYAXON_JOB_SIDECAR_CONTAINER_NAME')
JOB_DOCKER_NAME = config.get_string('POLYAXON_JOB_DOCKER_NAME',
                                    is_optional=True) or 'polyaxon/polyaxon-lib:0.0.1'
JOB_SIDECAR_DOCKER_IMAGE = config.get_string('POLYAXON_JOB_SIDECAR_DOCKER_IMAGE',
                                             is_optional=True) or 'polyaxon/polyaxon-api:0.0.1'
