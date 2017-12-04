# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime

import factory
from faker import Factory as FakerFactory

from spawner.utils.constants import NodeRoles

from clusters.models import Cluster, NodeGPU, ClusterNode, ClusterEvent
from tests.factories.factory_users import UserFactory

fake = FakerFactory.create()


class ClusterFactory(factory.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    version_api = factory.Sequence(lambda i: {
        'build_date': '{}'.format(str(datetime.datetime.now())),
        'compiler': 'gc',
        'git_commit': '17d7182a7ccbb167074be7a87f0a68bd00d58d9{}'.format(i),
        'git_tree_state': 'clean',
        'git_version': 'v1.7.5',
        'go_version': 'go1.8.3',
        'major': '1',
        'minor': '7',
        'platform': 'linux/amd64'})

    class Meta:
        model = Cluster


class ClusterNodeFactory(factory.DjangoModelFactory):
    role = NodeRoles.MASTER
    kubelet_version = 'v1.7.5'
    os_image = 'Buildroot 2017.02'
    kernel_version = '4.9.13'
    memory = factory.Sequence(lambda x: x)
    n_cpus = factory.Sequence(lambda x: x)
    n_gpus = factory.Sequence(lambda x: x)

    cluster = factory.SubFactory(ClusterFactory)

    class Meta:
        model = ClusterNode


class GPUFactory(factory.DjangoModelFactory):
    serial = factory.Sequence(lambda i: '{}'.format(i))
    name = factory.Sequence(lambda i: 'Tesla-{}'.format(i))
    memory = factory.Sequence(lambda x: x)
    device = factory.Sequence(lambda i: '/dev/nvidia{}'.format(i))

    cluster_node = factory.SubFactory(ClusterNodeFactory)

    class Meta:
        model = NodeGPU


class ClusterEventFactory(factory.DjangoModelFactory):
    level = 'error'
    data = factory.Sequence(lambda i: {'data': i})
    meta = factory.Sequence(lambda i: {'meta': i})

    cluster = factory.SubFactory(ClusterFactory)

    class Meta:
        model = ClusterEvent
