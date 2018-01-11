# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from polyaxon.utils import config

# Roles
ROLE_LABELS_WORKER = config.get_string('POLYAXON_ROLE_LABELS_WORKER')
ROLE_LABELS_DASHBOARD = config.get_string('POLYAXON_ROLE_LABELS_DASHBOARD')
ROLE_LABELS_LOG = config.get_string('POLYAXON_ROLE_LABELS_LOG')
ROLE_LABELS_API = config.get_string('POLYAXON_ROLE_LABELS_API')
K8S_SERVICE_ACCOUNT_NAME = config.get_string('POLYAXON_K8S_SERVICE_ACCOUNT_NAME')

# Types
TYPE_LABELS_CORE = config.get_string('POLYAXON_TYPE_LABELS_CORE')
TYPE_LABELS_EXPERIMENT = config.get_string('POLYAXON_TYPE_LABELS_EXPERIMENT')

# Selectors
NODE_SELECTORS_EXPERIMENTS = config.get_string('POLYAXON_NODE_SELECTORS_EXPERIMENTS',
                                               is_optional=True)

JOB_CONTAINER_NAME = config.get_string('POLYAXON_JOB_CONTAINER_NAME')
JOB_SIDECAR_CONTAINER_NAME = config.get_string('POLYAXON_JOB_SIDECAR_CONTAINER_NAME')
JOB_DOCKER_NAME = config.get_string('POLYAXON_JOB_DOCKER_NAME',
                                    is_optional=True) or 'polyaxon/polyaxon-lib'
JOB_SIDECAR_DOCKER_IMAGE = config.get_string('POLYAXON_JOB_SIDECAR_DOCKER_IMAGE',
                                             is_optional=True) or 'polyaxon/polyaxon-sidecar'
JOB_SIDECAR_LOG_SLEEP_INTERVAL = config.get_int('POLYAXON_JOB_SIDECAR_LOG_SLEEP_INTERVAL',
                                                is_optional=True)
JOB_SIDECAR_PERSIST = config.get_boolean('POLYAXON_JOB_SIDECAR_PERSIST',
                                         is_optional=True)
