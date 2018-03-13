# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import base64
import json

from django.conf import settings
from kubernetes import client

from polyaxon_k8s import constants as k8s_constants

from experiments.paths import get_experiment_outputs_path, get_experiment_logs_path
from projects.paths import get_project_data_path
from spawners.templates import constants


def get_env_var(name, value, reraise=True):
    if not isinstance(value, str):
        try:
            value = json.dumps(value)
        except (ValueError, TypeError) as e:
            if reraise:
                raise e

    return client.V1EnvVar(name=name, value=value)


def get_map_labels(project_name,
                   experiment_group_name,
                   experiment_name,
                   project_uuid,
                   experiment_group_uuid,
                   experiment_uuid):
    labels = {'project_name': project_name,
              'experiment_group_name': experiment_group_name,
              'experiment_name': experiment_name,
              'project_uuid': project_uuid,
              'experiment_uuid': experiment_uuid}
    if experiment_group_uuid:
        labels['experiment_group_uuid'] = experiment_group_uuid

    return labels


def get_config_map(namespace,
                   project_name,
                   experiment_group_name,
                   experiment_name,
                   project_uuid,
                   experiment_group_uuid,
                   experiment_uuid,
                   cluster_def,
                   declarations,
                   log_level):
    name = constants.CONFIG_MAP_NAME.format(experiment_uuid=experiment_uuid)
    labels = get_map_labels(project_name,
                            experiment_group_name,
                            experiment_name,
                            project_uuid,
                            experiment_group_uuid,
                            experiment_uuid)
    metadata = client.V1ObjectMeta(name=name, labels=labels, namespace=namespace)
    experiment_outputs_path = get_experiment_outputs_path(experiment_name)
    experiment_logs_path = get_experiment_logs_path(experiment_name)
    experiment_data_path = get_project_data_path(project_name)
    data = {
        constants.CONFIG_MAP_CLUSTER_KEY_NAME: json.dumps(cluster_def),
        constants.CONFIG_MAP_DECLARATIONS_KEY_NAME: json.dumps(declarations) or '{}',
        constants.CONFIG_MAP_EXPERIMENT_INFO_KEY_NAME: json.dumps(labels),
        constants.CONFIG_MAP_LOG_LEVEL_KEY_NAME: log_level,
        constants.CONFIG_MAP_API_KEY_NAME: 'http://{}:{}'.format(settings.POLYAXON_K8S_API_HOST,
                                                                 settings.POLYAXON_K8S_API_PORT),
        constants.CONFIG_MAP_EXPERIMENT_OUTPUTS_PATH_KEY_NAME: experiment_outputs_path,
        constants.CONFIG_MAP_EXPERIMENT_LOGS_PATH_KEY_NAME: experiment_logs_path,
        constants.CONFIG_MAP_EXPERIMENT_DATA_PATH_KEY_NAME: experiment_data_path,
    }
    return client.V1ConfigMap(api_version=k8s_constants.K8S_API_VERSION_V1,
                              kind=k8s_constants.K8S_CONFIG_MAP_KIND,
                              metadata=metadata,
                              data=data)


def get_secret(namespace,
               project_name,
               experiment_group_name,
               experiment_name,
               project_uuid,
               experiment_group_uuid,
               experiment_uuid,
               user_token):
    name = constants.SECRET_NAME.format(experiment_uuid=experiment_uuid)
    labels = get_map_labels(project_name,
                            experiment_group_name,
                            experiment_name,
                            project_uuid,
                            experiment_group_uuid,
                            experiment_uuid)
    metadata = client.V1ObjectMeta(name=name, labels=labels, namespace=namespace)
    data = {
        constants.SECRET_USER_TOKEN: base64.b64encode(bytes(user_token, 'utf-8')).decode("utf-8")
    }
    return client.V1Secret(api_version=k8s_constants.K8S_API_VERSION_V1,
                           kind=k8s_constants.K8S_SECRET_KIND,
                           metadata=metadata,
                           type="Opaque",
                           data=data)
