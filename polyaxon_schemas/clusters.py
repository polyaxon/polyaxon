# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load, post_dump

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.utils import UUID


class NodeGPUSchema(Schema):
    uuid = UUID()
    serial = fields.Str()
    name = fields.Str()
    device = fields.Str()
    memory = fields.Int()
    cluster_node = UUID()

    @post_load
    def make(self, data):
        return NodeGPUConfig(**data)

    @post_dump
    def unmake(self, data):
        return NodeGPUConfig.remove_reduced_attrs(data)


class NodeGPUConfig(BaseConfig):
    SCHEMA = NodeGPUSchema
    IDENTIFIER = 'NodeGPU'

    def __init__(self, uuid, serial, name, device, memory, cluster_node):
        self.uuid = uuid
        self.serial = serial
        self.name = name
        self.device = device
        self.memory = memory
        self.cluster_node = cluster_node


class ClusterNodeSchema(Schema):
    uuid = UUID()
    name = fields.Str(allow_none=True)
    hostname = fields.Str(allow_none=True)
    role = fields.Str(allow_none=True)
    docker_version = fields.Str(allow_none=True)
    kubelet_version = fields.Str(allow_none=True)
    os_image = fields.Str(allow_none=True)
    kernel_version = fields.Str(allow_none=True)
    schedulable_taints = fields.Bool(allow_none=True)
    schedulable_state = fields.Bool(allow_none=True)
    memory = fields.Int(allow_none=True)
    n_cpus = fields.Int(allow_none=True)
    n_gpus = fields.Int(allow_none=True)
    status = fields.Str(allow_none=True)
    gpus = fields.Nested(NodeGPUSchema, many=True, allow_none=True)

    @post_load
    def make(self, data):
        return ClusterNodeConfig(**data)

    @post_dump
    def unmake(self, data):
        return ClusterNodeConfig.remove_reduced_attrs(data)


class ClusterNodeConfig(BaseConfig):
    SCHEMA = ClusterNodeSchema
    IDENTIFIER = 'ClusterNode'
    REDUCED_ATTRIBUTES = ['docker_version', 'kubelet_version', 'os_image',
                          'schedulable_taints', 'schedulable_state', 'gpus']

    def __init__(self,
                 uuid,
                 name=None,
                 hostname=None,
                 role=None,
                 docker_version=None,
                 kubelet_version=None,
                 os_image=None,
                 kernel_version=None,
                 schedulable_taints=None,
                 schedulable_state=None,
                 memory=None,
                 n_cpus=None,
                 n_gpus=None,
                 status=None,
                 gpus=None):
        self.uuid = uuid
        self.name = name
        self.hostname = hostname
        self.role = role
        self.docker_version = docker_version
        self.kubelet_version = kubelet_version
        self.os_image = os_image
        self.kernel_version = kernel_version
        self.schedulable_taints = schedulable_taints
        self.schedulable_state = schedulable_state
        self.memory = memory
        self.n_cpus = n_cpus
        self.n_gpus = n_gpus
        self.status = status
        self.gpus = gpus


class PolyaxonClusterSchema(Schema):
    version_api = fields.Dict()
    nodes = fields.Nested(ClusterNodeSchema, many=True, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return PolyaxonClusterConfig(**data)

    @post_dump
    def unmake(self, data):
        return PolyaxonClusterConfig.remove_reduced_attrs(data)


class PolyaxonClusterConfig(BaseConfig):
    """Polyaxon cluster definition"""
    SCHEMA = PolyaxonClusterSchema
    IDENTIFIER = 'PolyaxonCluster'

    def __init__(self, version_api, nodes=None):
        self.version_api = version_api
        self.nodes = nodes
