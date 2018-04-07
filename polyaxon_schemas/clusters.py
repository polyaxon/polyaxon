# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_dump, post_load

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.utils import UUID


class NodeGPUSchema(Schema):
    index = fields.Int()
    name = fields.Str()
    uuid = UUID()
    memory = fields.Int()
    serial = fields.Str()
    cluster_node = UUID()

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return NodeGPUConfig(**data)

    @post_dump
    def unmake(self, data):
        return NodeGPUConfig.remove_reduced_attrs(data)


class NodeGPUConfig(BaseConfig):
    SCHEMA = NodeGPUSchema
    IDENTIFIER = 'NodeGPU'
    DEFAULT_EXCLUDE_ATTRIBUTES = ['uuid', 'cluster_node']

    def __init__(self, index, name, uuid, memory, serial, cluster_node):
        self.uuid = uuid
        self.serial = serial
        self.name = name
        self.index = index
        self.memory = memory
        self.cluster_node = cluster_node


class ClusterNodeSchema(Schema):
    sequence = fields.Int(allow_none=True)
    name = fields.Str(allow_none=True)
    uuid = UUID()
    status = fields.Str(allow_none=True)
    hostname = fields.Str(allow_none=True)
    role = fields.Str(allow_none=True)
    memory = fields.Int(allow_none=True)
    cpu = fields.Float(allow_none=True)
    n_gpus = fields.Int(allow_none=True)
    kubelet_version = fields.Str(allow_none=True)
    docker_version = fields.Str(allow_none=True)
    os_image = fields.Str(allow_none=True)
    kernel_version = fields.Str(allow_none=True)
    schedulable_taints = fields.Bool(allow_none=True)
    schedulable_state = fields.Bool(allow_none=True)
    gpus = fields.Nested(NodeGPUSchema, many=True, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ClusterNodeConfig(**data)

    @post_dump
    def unmake(self, data):
        return ClusterNodeConfig.remove_reduced_attrs(data)


class ClusterNodeConfig(BaseConfig):
    SCHEMA = ClusterNodeSchema
    IDENTIFIER = 'ClusterNode'
    DEFAULT_INCLUDE_ATTRIBUTES = [
        'sequence', 'name', 'hostname', 'role', 'memory', 'cpu', 'n_gpus', 'status'
    ]

    def __init__(self,
                 uuid,
                 sequence=None,
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
                 cpu=None,
                 n_gpus=None,
                 status=None,
                 gpus=None):
        self.uuid = uuid
        self.sequence = sequence
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
        self.cpu = cpu
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
