# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import logging
import uuid

import requests
from django.conf import settings
from polyaxon_k8s.manager import K8SManager

from polyaxon.celery_api import app as celery_app
from polyaxon.settings import CeleryTasks
from clusters.models import Cluster, ClusterNode

logger = logging.getLogger('polyaxon.tasks.clusters')


@celery_app.task(name=CeleryTasks.CLUSTERS_UPDATE_SYSTEM_INFO, time_limit=150, ignore_result=True)
def update_system_info():

    k8s_manager = K8SManager(in_cluster=True)
    version_api = k8s_manager.get_version()
    cluster = Cluster.load()
    if cluster.version_api != version_api:
        cluster.version_api = version_api
        cluster.save()


@celery_app.task(name=CeleryTasks.CLUSTERS_UPDATE_SYSTEM_NODES, time_limit=150, ignore_result=True)
def update_system_nodes():

    k8s_manager = K8SManager(in_cluster=True)
    nodes = k8s_manager.list_nodes()
    cluster = Cluster.load()
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


@celery_app.task(name=CeleryTasks.CLUSTERS_NOTIFICATION_ALIVE, time_limits=60, ignore_result=True)
def cluster_analytics():
    cluster_uuid = Cluster.load().uuid.hex
    notification = uuid.uuid4()
    notification_url = settings.POLYAXON_NOTIFICATION_ALIVE_URL.format(
        cluster_uuid=cluster_uuid,
        notification=notification,
        version=settings.CHART_VERSION)
    try:
        requests.get(notification_url)
    except requests.RequestException:
        pass
