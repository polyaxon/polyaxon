# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from polyaxon_k8s.utils import nodes
from polyaxon_k8s import constants as k8s_constants

from libs.models import DiffModel


class Cluster(DiffModel):
    """A model that represents the cluster api version."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='clusters')
    version_api = JSONField(help_text='The cluster version api infos')


class ClusterNode(models.Model):
    """A model that represents the cluster node."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    name = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        help_text='Name of the node')
    cluster = models.ForeignKey(Cluster, related_name='nodes')
    hostname = models.CharField(
        max_length=256,
        blank=True,
        null=True)
    role = models.CharField(
        max_length=6,
        choices=k8s_constants.NodeRoles.CHOICES,
        help_text='The role of the node')
    docker_version = models.CharField(
        max_length=128,
        blank=True,
        null=True)
    kubelet_version = models.CharField(
        max_length=10)
    os_image = models.CharField(max_length=128)
    kernel_version = models.CharField(max_length=128)
    schedulable_taints = models.BooleanField(default=False)
    schedulable_state = models.BooleanField(default=False)
    memory = models.BigIntegerField()
    n_cpus = models.SmallIntegerField()
    n_gpus = models.SmallIntegerField()
    status = models.CharField(
        max_length=24,
        default=k8s_constants.NodeLifeCycle.UNKNOWN,
        choices=k8s_constants.NodeLifeCycle.CHOICES)
    is_current = models.BooleanField(default=True)

    @classmethod
    def from_node_item(cls, node):
        params = {
            'name': node.metadata.name,
            'hostname': nodes.get_hostname(node),
            'role': nodes.get_role(node),
            'docker_version': nodes.get_docker_version(node),
            'kubelet_version': node.status.node_info.kubelet_version,
            'os_image': node.status.node_info.os_image,
            'kernel_version': node.status.node_info.kernel_version,
            'schedulable_taints': nodes.is_schedulable(node),
            'schedulable_state': nodes.get_schedulable_state(node),
            'mem': nodes.get_memory_size(node),
            'n_cpus': nodes.get_n_cpus(node),
            'n_gpus': nodes.get_n_gpus(node),
            'status': nodes.get_status(node)}

        return cls(**params)


class NodeGPU(DiffModel):
    """A model that represents the node's gpu."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    serial = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    device = models.CharField(max_length=256)
    memory = models.BigIntegerField()
    cluster_node = models.ForeignKey(ClusterNode, related_name='gpus')


class ClusterEvents(models.Model):
    """A model to catch all errors and warning events of the cluster."""
    cluster = models.ForeignKey(Cluster, related_name='errors')
    created_at = models.DateTimeField()
    data = JSONField()
    meta = JSONField()
    level = models.CharField(max_length=16)
