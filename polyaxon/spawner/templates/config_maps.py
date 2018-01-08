# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json

from kubernetes import client

from polyaxon_k8s import constants as k8s_constants

from experiments.utils import get_experiment_outputs_path
from spawner.templates import constants


def get_config_map_labels(project_name,
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
                   declarations):
    name = constants.CONFIG_MAP_NAME.format(experiment_uuid=experiment_uuid)
    labels = get_config_map_labels(project_name,
                                   experiment_group_name,
                                   experiment_name,
                                   project_uuid,
                                   experiment_group_uuid,
                                   experiment_uuid)
    metadata = client.V1ObjectMeta(name=name, labels=labels, namespace=namespace)
    experiment_outputs_path = get_experiment_outputs_path(experiment_name)
    data = {
        constants.CONFIG_MAP_CLUSTER_KEY_NAME: json.dumps(cluster_def),
        constants.CONFIG_MAP_DECLARATIONS_KEY_NAME: json.dumps(declarations) or '{}',
        constants.CONFIG_MAP_EXPERIMENT_INFO_KEY_NAME: json.dumps(labels),
        constants.CONFIG_MAP_EXPERIMENT_OUTPUTS_PATH_KEY_NAME: experiment_outputs_path
    }
    return client.V1ConfigMap(api_version=k8s_constants.K8S_API_VERSION_V1,
                              kind=k8s_constants.K8S_CONFIG_MAP_KIND,
                              metadata=metadata,
                              data=data)
