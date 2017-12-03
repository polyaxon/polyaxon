# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from kubernetes import client

from polyaxon_k8s import constants as k8s_constants

from polyaxon_spawner.templates import constants


def get_cluster_config_map_labels(project, experiment, role):
    return {'project': project,
            'experiment': '{}'.format(experiment),
            'role': role}


def get_cluster_config_map(namespace, project, experiment, cluster_def):
    def convert_cluster_def():
        return {k: ','.join(v) for k, v in six.iteritems(cluster_def)}

    name = constants.CONFIG_MAP_NAME.format(project=project,
                                            experiment=experiment,
                                            role='cluster')
    labels = get_cluster_config_map_labels(project, experiment, 'cluster')
    metadata = client.V1ObjectMeta(name=name, labels=labels, namespace=namespace)
    return client.V1ConfigMap(api_version=k8s_constants.K8S_API_VERSION_V1,
                              kind=k8s_constants.K8S_CONFIG_MAP_KIND,
                              metadata=metadata,
                              data=convert_cluster_def())
