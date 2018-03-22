import uuid

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.core.cache import cache
from django.db import models

from libs.models import DiffModel, Singleton
from spawners.utils import nodes
from spawners.utils.constants import NodeLifeCycle, NodeRoles


class Cluster(Singleton):
    """A model that represents the cluster api version."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    version_api = JSONField(help_text='The cluster version api infos')

    def __str__(self):
        return 'Cluster: {}'.format(self.uuid.hex)

    @classmethod
    def may_be_update(cls, obj):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            try:
                obj = cls.objects.get(pk=1)
            except cls.DoesNotExist:
                params = {'version_api': {}}
                if settings.CLUSTER_ID:
                    params['uuid'] = settings.CLUSTER_ID
                obj = cls.objects.create(pk=1, **params)
                obj.set_cache()
        else:
            obj = cache.get(cls.__name__)
        return obj


class ClusterNode(models.Model):
    """A model that represents the cluster node."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    sequence = models.PositiveSmallIntegerField(
        editable=False,
        null=False,
        help_text='The sequence number of this node within the cluser.', )
    name = models.CharField(
        max_length=256,
        null=False,
        help_text='Name of the node')
    cluster = models.ForeignKey(
        Cluster,
        on_delete=models.CASCADE,
        related_name='nodes')
    hostname = models.CharField(
        max_length=256,
        blank=True,
        null=True)
    role = models.CharField(
        max_length=6,
        choices=NodeRoles.CHOICES,
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
    cpu = models.FloatField()
    n_gpus = models.PositiveSmallIntegerField()
    status = models.CharField(
        max_length=24,
        default=NodeLifeCycle.UNKNOWN,
        choices=NodeLifeCycle.CHOICES)
    is_current = models.BooleanField(default=True)

    class Meta:
        ordering = ['sequence']
        unique_together = (('cluster', 'sequence'),)

    def __str__(self):
        return '{}/{}'.format(self.cluster, self.name)

    def save(self, *args, **kwargs):
        if self.pk is None:
            last = ClusterNode.objects.filter(cluster=self.cluster).last()
            self.sequence = 1
            if last:
                self.sequence = last.sequence + 1

        super(ClusterNode, self).save(*args, **kwargs)

    @classmethod
    def from_node_item(cls, node):
        return {
            'name': node.metadata.name,
            'hostname': nodes.get_hostname(node),
            'role': nodes.get_role(node),
            'docker_version': nodes.get_docker_version(node),
            'kubelet_version': node.status.node_info.kubelet_version,
            'os_image': node.status.node_info.os_image,
            'kernel_version': node.status.node_info.kernel_version,
            'schedulable_taints': nodes.is_schedulable(node),
            'schedulable_state': nodes.get_schedulable_state(node),
            'memory': nodes.get_memory(node),
            'cpu': nodes.get_cpu(node),
            'n_gpus': nodes.get_n_gpus(node),
            'status': nodes.get_status(node)}


class NodeGPU(DiffModel):
    """A model that represents the node's gpu."""
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=False)
    index = models.PositiveSmallIntegerField()
    serial = models.CharField(max_length=256)
    name = models.CharField(max_length=256)
    memory = models.BigIntegerField()
    cluster_node = models.ForeignKey(
        ClusterNode,
        on_delete=models.CASCADE,
        related_name='gpus')

    class Meta:
        ordering = ['index']
        unique_together = (('cluster_node', 'index'),)

    def __str__(self):
        return self.serial


class ClusterEvent(models.Model):
    """A model to catch all errors and warning events of the cluster."""
    cluster = models.ForeignKey(
        Cluster,
        on_delete=models.CASCADE,
        related_name='events')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    data = JSONField()
    meta = JSONField()
    level = models.CharField(max_length=16)

    def __str__(self):
        return 'Event {} at {}'.format(self.level, self.created_at)
