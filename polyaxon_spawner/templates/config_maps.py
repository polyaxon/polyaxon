# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import six

from kubernetes import client

from polyaxon_spawner.templates import constants


def get_cluster_config_map(project, experiment, cluster_def):
    def convert_cluster_def():
        return {k: ','.join(v) for k, v in six.iteritems(cluster_def)}

    name = constants.CONFIG_MAP_CLUSTER_NAME.format(project=project, experiment=experiment)
    metadata = client.V1ObjectMeta(
        name=name, labels={'project': project, 'experiment': '{}'.format(experiment)})
    return client.V1ConfigMap(api_version=constants.K8S_API_VERSION_V1,
                              kind=constants.K8S_CONFIG_MAP_KIND,
                              metadata=metadata,
                              data=convert_cluster_def())
