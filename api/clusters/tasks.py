# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging

from polyaxon_k8s.manager import K8SManager

from api.settings import CeleryTasks
from api.celery_api import app as celery_app
from clusters.utils import get_cluster
from clusters.models import ClusterNode

logger = logging.getLogger('polyaxon.tasks.clusters')


@celery_app.task(name=CeleryTasks.CLUSTERS_UPDATE_SYSTEM_INFO, time_limit=150)
def update_system_info():

    k8s_manager = K8SManager(in_cluster=True)
    version_api = k8s_manager.get_version()
    cluster = get_cluster()
    if cluster.version_api != version_api:
        cluster.version_api = version_api
        cluster.save()


@celery_app.task(name=CeleryTasks.CLUSTERS_UPDATE_SYSTEM_NODES, time_limit=150)
def update_system_nodes():

    k8s_manager = K8SManager(in_cluster=True)
    nodes = k8s_manager.list_nodes()
    cluster = get_cluster()
    nodes_to_update = {}
    nodes_to_create = {node.metadata.name: node for node in nodes}
    deprecated_nodes = []
    for node in cluster.nodes.all():
        if node.name in nodes_to_create:
            nodes_to_update[node.name] = (node, nodes_to_create.pop(node.name))
        else:
            deprecated_nodes.append(node)

    for node in deprecated_nodes:
        node.is_current = False
        node.save()

    for node in nodes_to_create.values():
        node_dict = ClusterNode.from_node_item(node)
        node_dict['cluster'] = cluster
        ClusterNode.objects.create(**node_dict)

    for current_node, new_node in nodes_to_update.values():
        node_dict = ClusterNode.from_node_item(new_node)
        for k, v in node_dict.items():
            setattr(current_node, k, v)
            current_node.save()


@celery_app.task(name=CeleryTasks.CLUSTERS_UPDATE_SYSTEM_NODES_GPUS, time_limit=150)
def update_system_node_gpus():
    pass
