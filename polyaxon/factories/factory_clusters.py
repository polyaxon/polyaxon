from faker import Factory as FakerFactory

import factory

from constants.nodes import NodeRoles
from db.models.clusters import Cluster
from db.models.nodes import ClusterEvent, ClusterNode, NodeGPU

fake = FakerFactory.create()


class ClusterNodeFactory(factory.DjangoModelFactory):
    role = NodeRoles.MASTER
    kubelet_version = 'v1.7.5'
    os_image = 'Buildroot 2017.02'
    kernel_version = '4.9.13'
    name = factory.Sequence('name {}'.format)
    memory = factory.Sequence(lambda x: x)
    cpu = factory.Sequence(lambda x: x)
    n_gpus = factory.Sequence(lambda x: x)

    class Meta:
        model = ClusterNode


def get_cluster_node(**kwargs):
    cluster = Cluster.load()
    return ClusterNodeFactory(cluster=cluster, **kwargs)


class GPUFactory(factory.DjangoModelFactory):
    serial = factory.Sequence('{}'.format)
    name = factory.Sequence('Tesla-{}'.format)
    memory = factory.Sequence(lambda x: x)
    index = factory.Sequence(lambda i: i)

    cluster_node = factory.SubFactory(ClusterNodeFactory)

    class Meta:
        model = NodeGPU


def get_gpu(**kwargs):
    if not kwargs.get('cluster_node'):
        cluster = Cluster.load()
        cluster['cluster_node'] = ClusterNodeFactory(cluster=cluster, **kwargs)

    return GPUFactory(**kwargs)


class ClusterEventFactory(factory.DjangoModelFactory):
    level = 'error'
    data = factory.Sequence(lambda i: {'data': i})
    meta = factory.Sequence(lambda i: {'meta': i})

    class Meta:
        model = ClusterEvent
