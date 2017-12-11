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
    cluster = UUID()
    hostname = fields.Str(allow_none=True)
    role = fields.Str()
    docker_version = fields.Str(allow_none=True)
    kubelet_version = fields.Str()
    os_image = fields.Str()
    kernel_version = fields.Str()
    schedulable_taints = fields.Bool()
    schedulable_state = fields.Bool()
    memory = fields.Int()
    n_cpus = fields.Int()
    n_gpus = fields.Int()
    status = fields.Str()
    gpus = fields.Nested(NodeGPUSchema, many=True)

    @post_load
    def make(self, data):
        return ClusterNodeConfig(**data)

    @post_dump
    def unmake(self, data):
        return ClusterNodeConfig.remove_reduced_attrs(data)


class ClusterNodeConfig(BaseConfig):
    SCHEMA = ClusterNodeSchema
    IDENTIFIER = 'ClusterNode'

    def __init__(self,
                 uuid,
                 name,
                 cluster,
                 hostname,
                 role,
                 docker_version,
                 kubelet_version,
                 os_image,
                 kernel_version,
                 schedulable_taints,
                 schedulable_state,
                 memory,
                 n_cpus,
                 n_gpus,
                 status,
                 gpus=None):
        self.uuid = uuid
        self.name = name
        self.cluster = cluster
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
    uuid = UUID()
    user = UUID()
    version_api = fields.Dict()
    nodes = fields.Nested(ClusterNodeSchema, many=True)

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

    def __init__(self, uuid, user, version_api, nodes=None):
        self.uuid = uuid
        self.user = user
        self.version_api = version_api
        self.nodes = nodes
