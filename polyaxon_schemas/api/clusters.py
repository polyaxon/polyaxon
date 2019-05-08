# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.fields import UUID


class NodeGPUSchema(BaseSchema):
    index = fields.Int()
    name = fields.Str()
    uuid = UUID()
    memory = fields.Int()
    serial = fields.Str()
    cluster_node = UUID()

    @staticmethod
    def schema_config():
        return NodeGPUConfig


class NodeGPUConfig(BaseConfig):
    """
    Node gpu config.

    Args:
        index: `int`. The index of the gpu during the discovery.
        name: `str`. The name of gpu.
        uuid: `UUID`. The uuid of gpu.
        memory: `int`. The memory size of the gpu.
        serial: `str`. The serial of the gpu.
        cluster_node: `UUID`. the uuid of the cluster node.
    """
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


class ClusterNodeSchema(BaseSchema):
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

    @staticmethod
    def schema_config():
        return ClusterNodeConfig


class ClusterNodeConfig(BaseConfig):
    """
    Node gpu config.

    Args:
        uuid: `UUID`. the uuid of the cluster node.
        sequence: `int`. The sequence of the node in the cluster.
        name: `str`. The name of node.
        hostname: `str`. The node hostname.
        role: `str`. The role of the node.
        docker_version: `str`. The docker version used in the node.
        kubelet_version: `str`. The kubelet version used in the node.
        os_image: `str`. The os image used of the node.
        kernel_version: `str`. The kernel version of the node.
        schedulable_taints: `bool`. The schedulable taints of the node.
        schedulable_state: `bool`. The schedulable state of the node.
        memory: `int`. The memory size of the node.
        cpu: `float`. The cpu of the node.
        n_gpus: `int`. The number of gpus in the node.
        status: `str`. The status of the node (ready or ...)
        gpus: `list(NodeGPUConfig)`. The node gpus.
    """
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


class PolyaxonClusterSchema(BaseSchema):
    version_api = fields.Dict()
    nodes = fields.Nested(ClusterNodeSchema, many=True, allow_none=True)

    @staticmethod
    def schema_config():
        return PolyaxonClusterConfig


class PolyaxonClusterConfig(BaseConfig):
    """
    Polyaxon cluster config.

    Args:
        version_api: `dict`. The cluster's version api.
        nodes: list(ClusterNodeConfig). The nodes in the cluster.
    """
    SCHEMA = PolyaxonClusterSchema
    IDENTIFIER = 'PolyaxonCluster'

    def __init__(self, version_api, nodes=None):
        self.version_api = version_api
        self.nodes = nodes
