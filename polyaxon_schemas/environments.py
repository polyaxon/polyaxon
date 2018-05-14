# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, ValidationError, fields, post_dump, post_load, validates_schema

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.utils import UUID


class TensorflowClusterSchema(Schema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)
    ps = fields.List(fields.Str(), allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return TensorflowClusterConfig(**data)

    @post_dump
    def unmake(self, data):
        return TensorflowClusterConfig.remove_reduced_attrs(data)


class TensorflowClusterConfig(BaseConfig):
    """Tensorflow cluster definition"""
    IDENTIFIER = 'tensorflow_cluster'
    SCHEMA = TensorflowClusterSchema

    def __init__(self, master=None, worker=None, ps=None):
        self.master = master
        self.worker = worker
        self.ps = ps


class HorovodClusterSchema(Schema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return HorovodClusterConfig(**data)

    @post_dump
    def unmake(self, data):
        return HorovodClusterConfig.remove_reduced_attrs(data)


class HorovodClusterConfig(BaseConfig):
    """Horovod cluster definition"""
    IDENTIFIER = 'horovod_cluster'
    SCHEMA = HorovodClusterSchema

    def __init__(self, master=None, worker=None):
        self.master = master
        self.worker = worker


class PytorchClusterSchema(Schema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return PytorchClusterConfig(**data)

    @post_dump
    def unmake(self, data):
        return PytorchClusterConfig.remove_reduced_attrs(data)


class PytorchClusterConfig(BaseConfig):
    """Pytorch cluster definition"""
    IDENTIFIER = 'pytorch_cluster'
    SCHEMA = PytorchClusterSchema

    def __init__(self, master=None, worker=None):
        self.master = master
        self.worker = worker


class MXNetClusterSchema(Schema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)
    server = fields.List(fields.Str(), allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return MXNetClusterConfig(**data)

    @post_dump
    def unmake(self, data):
        return MXNetClusterConfig.remove_reduced_attrs(data)


class MXNetClusterConfig(BaseConfig):
    """MXNet cluster definition"""
    IDENTIFIER = 'mxnet_cluster'
    SCHEMA = MXNetClusterSchema

    def __init__(self, master=None, worker=None, server=None):
        self.master = master
        self.worker = worker
        self.server = server


class K8SResourcesSchema(Schema):
    limits = fields.Float(allow_none=True)
    requests = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return K8SResourcesConfig(**data)

    @post_dump
    def unmake(self, data):
        return K8SResourcesConfig.remove_reduced_attrs(data)


class K8SResourcesConfig(BaseConfig):
    IDENTIFIER = 'resources'
    SCHEMA = K8SResourcesSchema

    def __init__(self, limits=None, requests=None):
        self.limits = limits
        self.requests = requests

    def __add__(self, other):
        if not other:
            return self

        if self.requests:
            if other.requests:
                self.requests += other.requests
        elif other.requests:
            self.requests = other.requests

        if self.limits:
            if other.limits:
                self.limits += other.limits
        elif other.limits:
            self.limits = other.limits

        return self


class PodResourcesSchema(Schema):
    # To indicate which worker/ps index this session config belongs to
    index = fields.Int(allow_none=True)
    cpu = fields.Nested(K8SResourcesSchema, allow_none=True)
    memory = fields.Nested(K8SResourcesSchema, allow_none=True)
    gpu = fields.Nested(K8SResourcesSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return PodResourcesConfig(**data)

    @post_dump
    def unmake(self, data):
        return PodResourcesConfig.remove_reduced_attrs(data)


class PodResourcesConfig(BaseConfig):
    IDENTIFIER = 'pod_resources'
    SCHEMA = PodResourcesSchema
    REDUCED_ATTRIBUTES = ['index']

    def __init__(self, index=None, cpu=None, memory=None, gpu=None):
        self.index = index
        self.cpu = cpu
        self.memory = memory
        self.gpu = gpu

    def __add__(self, other):
        if not other:
            return self

        if self.cpu:
            if other.cpu:
                self.cpu += other.cpu
        elif other.cpu:
            self.cpu = K8SResourcesConfig()
            self.cpu += other.cpu

        if self.memory:
            if other.memory:
                self.memory += other.memory
        elif other.memory:
            self.memory = K8SResourcesConfig()
            self.memory += other.memory

        if self.gpu:
            if other.gpu:
                self.gpu += other.gpu
        elif other.gpu:
            self.gpu = K8SResourcesConfig()
            self.gpu += other.gpu
        return self


class GPUOptionsSchema(Schema):
    gpu_memory_fraction = fields.Float(allow_none=True)
    allow_growth = fields.Bool(allow_none=True)
    per_process_gpu_memory_fraction = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return GPUOptionsConfig(**data)

    @post_dump
    def unmake(self, data):
        return GPUOptionsConfig.remove_reduced_attrs(data)


class GPUOptionsConfig(BaseConfig):
    IDENTIFIER = 'session'
    SCHEMA = GPUOptionsSchema

    def __init__(self,
                 gpu_memory_fraction=None,
                 allow_growth=True,
                 per_process_gpu_memory_fraction=None):
        self.gpu_memory_fraction = gpu_memory_fraction
        self.allow_growth = allow_growth
        self.per_process_gpu_memory_fraction = per_process_gpu_memory_fraction


class SessionSchema(Schema):
    # To indicate which worker/ps index this session config belongs to
    index = fields.Int(allow_none=True)
    gpu_options = fields.Nested(GPUOptionsSchema, allow_none=True)
    log_device_placement = fields.Bool(allow_none=True)
    allow_soft_placement = fields.Bool(allow_none=True)
    intra_op_parallelism_threads = fields.Int(allow_none=True)
    inter_op_parallelism_threads = fields.Int(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return SessionConfig(**data)

    @post_dump
    def unmake(self, data):
        return SessionConfig.remove_reduced_attrs(data)


class SessionConfig(BaseConfig):
    IDENTIFIER = 'session'
    SCHEMA = SessionSchema
    REDUCED_ATTRIBUTES = ['index']

    def __init__(self,
                 index=None,
                 log_device_placement=True,
                 gpu_options=GPUOptionsConfig(),
                 allow_soft_placement=True,
                 intra_op_parallelism_threads=None,
                 inter_op_parallelism_threads=None):
        self.index = index
        self.gpu_options = gpu_options
        self.log_device_placement = log_device_placement
        self.allow_soft_placement = allow_soft_placement
        self.intra_op_parallelism_threads = intra_op_parallelism_threads
        self.inter_op_parallelism_threads = inter_op_parallelism_threads


class RunSchema(Schema):
    tf_random_seed = fields.Int(allow_none=True)
    save_summary_steps = fields.Int(allow_none=True)
    save_checkpoints_secs = fields.Int(allow_none=True)
    save_checkpoints_steps = fields.Int(allow_none=True)
    keep_checkpoint_max = fields.Int(allow_none=True)
    keep_checkpoint_every_n_hours = fields.Int(allow_none=True)

    session = fields.Nested(SessionSchema, allow_none=True)
    cluster = fields.Nested(TensorflowClusterSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return RunConfig(**data)

    @post_dump
    def unmake(self, data):
        return RunConfig.remove_reduced_attrs(data)


class RunConfig(BaseConfig):
    IDENTIFIER = 'run'
    SCHEMA = RunSchema

    def __init__(self,
                 tf_random_seed=None,
                 save_summary_steps=100,
                 save_checkpoints_secs=None,
                 save_checkpoints_steps=None,
                 keep_checkpoint_max=5,
                 keep_checkpoint_every_n_hours=10000,
                 session=None,
                 cluster=None):
        self.tf_random_seed = tf_random_seed
        self.save_summary_steps = save_summary_steps
        self.save_checkpoints_secs = save_checkpoints_secs
        self.save_checkpoints_steps = save_checkpoints_steps
        self.keep_checkpoint_max = keep_checkpoint_max
        self.keep_checkpoint_every_n_hours = keep_checkpoint_every_n_hours
        self.session = session
        self.cluster = cluster


class TensorflowSchema(Schema):
    n_workers = fields.Int(allow_none=True)
    n_ps = fields.Int(allow_none=True)
    delay_workers_by_global_step = fields.Bool(allow_none=True)
    run_config = fields.Nested(RunSchema, allow_none=True)
    default_worker_config = fields.Nested(SessionSchema, allow_none=True)
    default_worker_resources = fields.Nested(PodResourcesSchema, allow_none=True)
    default_worker_node_selectors = fields.Dict(allow_none=True)
    default_ps_config = fields.Nested(SessionSchema, allow_none=True)
    default_ps_resources = fields.Nested(PodResourcesSchema, allow_none=True)
    default_ps_node_selectors = fields.Dict(allow_none=True)
    worker_configs = fields.Nested(SessionSchema, many=True, allow_none=True)
    worker_resources = fields.Nested(PodResourcesSchema, many=True, allow_none=True)
    ps_configs = fields.Nested(SessionSchema, many=True, allow_none=True)
    ps_resources = fields.Nested(PodResourcesSchema, many=True, allow_none=True)
    worker_node_selectors = fields.List(fields.Dict(), allow_none=True)
    ps_node_selectors = fields.List(fields.Dict(), allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return TensorflowConfig(**data)

    @post_dump
    def unmake(self, data):
        return TensorflowConfig.remove_reduced_attrs(data)


class TensorflowConfig(BaseConfig):
    IDENTIFIER = 'tensorflow'
    SCHEMA = TensorflowSchema

    def __init__(self,
                 n_workers=0,
                 n_ps=0,
                 delay_workers_by_global_step=False,
                 run_config=None,
                 default_worker_config=None,
                 default_worker_resources=None,
                 default_ps_config=None,
                 default_ps_resources=None,
                 default_worker_node_selectors=None,
                 default_ps_node_selectors=None,
                 worker_configs=None,
                 worker_resources=None,
                 ps_configs=None,
                 ps_resources=None,
                 worker_node_selectors=None,
                 ps_node_selectors=None):
        self.n_workers = n_workers
        self.n_ps = n_ps
        self.delay_workers_by_global_step = delay_workers_by_global_step
        self.run_config = run_config
        self.default_worker_config = default_worker_config
        self.default_worker_resources = default_worker_resources
        self.default_ps_config = default_ps_config
        self.default_ps_resources = default_ps_resources
        self.default_worker_node_selectors = default_worker_node_selectors
        self.default_ps_node_selectors = default_ps_node_selectors
        self.worker_configs = worker_configs
        self.worker_resources = worker_resources
        self.ps_configs = ps_configs
        self.ps_resources = ps_resources
        self.worker_node_selectors = worker_node_selectors
        self.ps_node_selectors = ps_node_selectors


class HorovodSchema(Schema):
    n_workers = fields.Int(allow_none=True)
    default_worker_resources = fields.Nested(PodResourcesSchema, allow_none=True)
    default_worker_node_selectors = fields.Dict(allow_none=True)
    worker_resources = fields.Nested(PodResourcesSchema, many=True, allow_none=True)
    worker_node_selectors = fields.List(fields.Dict(allow_none=True), allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return HorovodConfig(**data)

    @post_dump
    def unmake(self, data):
        return HorovodConfig.remove_reduced_attrs(data)


class HorovodConfig(BaseConfig):
    IDENTIFIER = 'horovod'
    SCHEMA = HorovodSchema

    def __init__(self,
                 n_workers=0,
                 default_worker_resources=None,
                 default_worker_node_selectors=None,
                 worker_resources=None,
                 worker_node_selectors=None):
        self.n_workers = n_workers
        self.default_worker_resources = default_worker_resources
        self.default_worker_node_selectors = default_worker_node_selectors
        self.worker_resources = worker_resources
        self.worker_node_selectors = worker_node_selectors


class PytorchSchema(Schema):
    n_workers = fields.Int(allow_none=True)
    default_worker_resources = fields.Nested(PodResourcesSchema, allow_none=True)
    default_worker_node_selectors = fields.Dict(allow_none=True)
    worker_resources = fields.Nested(PodResourcesSchema, many=True, allow_none=True)
    worker_node_selectors = fields.List(fields.Dict(), allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return PytorchConfig(**data)

    @post_dump
    def unmake(self, data):
        return PytorchConfig.remove_reduced_attrs(data)


class PytorchConfig(BaseConfig):
    IDENTIFIER = 'pytorch'
    SCHEMA = PytorchSchema

    def __init__(self,
                 n_workers=0,
                 default_worker_resources=None,
                 default_worker_node_selectors=None,
                 worker_resources=None,
                 worker_node_selectors=None):
        self.n_workers = n_workers
        self.default_worker_resources = default_worker_resources
        self.default_worker_node_selectors = default_worker_node_selectors
        self.worker_resources = worker_resources
        self.worker_node_selectors = worker_node_selectors


class MXNetSchema(Schema):
    n_workers = fields.Int(allow_none=True)
    n_ps = fields.Int(allow_none=True)
    default_worker_resources = fields.Nested(PodResourcesSchema, allow_none=True)
    default_ps_resources = fields.Nested(PodResourcesSchema, allow_none=True)
    default_worker_node_selectors = fields.Dict(allow_none=True)
    default_ps_node_selectors = fields.Dict(allow_none=True)
    worker_resources = fields.Nested(PodResourcesSchema, many=True, allow_none=True)
    ps_resources = fields.Nested(PodResourcesSchema, many=True, allow_none=True)
    worker_node_selectors = fields.List(fields.Dict(), allow_none=True)
    ps_node_selectors = fields.List(fields.Dict(), allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return MXNetConfig(**data)

    @post_dump
    def unmake(self, data):
        return MXNetConfig.remove_reduced_attrs(data)


class MXNetConfig(BaseConfig):
    IDENTIFIER = 'mxnet'
    SCHEMA = MXNetSchema

    def __init__(self,
                 n_workers=0,
                 n_ps=0,
                 default_worker_resources=None,
                 default_ps_resources=None,
                 default_worker_node_selectors=None,
                 default_ps_node_selectors=None,
                 worker_resources=None,
                 ps_resources=None,
                 worker_node_selectors=None,
                 ps_node_selectors=None):
        self.n_workers = n_workers
        self.n_ps = n_ps
        self.default_worker_resources = default_worker_resources
        self.default_ps_resources = default_ps_resources
        self.default_worker_node_selectors = default_worker_node_selectors
        self.default_ps_node_selectors = default_ps_node_selectors
        self.worker_resources = worker_resources
        self.ps_resources = ps_resources
        self.worker_node_selectors = worker_node_selectors
        self.ps_node_selectors = ps_node_selectors


def validate_frameworks(frameworks):
    if sum([1 for f in frameworks if f is not None]) > 1:
        raise ValidationError('Only one framework can be used.')


class EnvironmentSchema(Schema):
    cluster_uuid = UUID(allow_none=True)
    resources = fields.Nested(PodResourcesSchema, allow_none=True)
    node_selectors = fields.Dict(allow_none=True)
    tensorflow = fields.Nested(TensorflowSchema, allow_none=True)
    horovod = fields.Nested(HorovodSchema, allow_none=True)
    mxnet = fields.Nested(MXNetSchema, allow_none=True)
    pytorch = fields.Nested(PytorchSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return EnvironmentConfig(**data)

    @post_dump
    def unmake(self, data):
        return EnvironmentConfig.remove_reduced_attrs(data)

    @validates_schema
    def validate_quantity(self, data):
        validate_frameworks([data.get('tensorflow'),
                             data.get('mxnet'),
                             data.get('pytorch'),
                             data.get('horovod')])


class EnvironmentConfig(BaseConfig):
    IDENTIFIER = 'environment'
    SCHEMA = EnvironmentSchema

    def __init__(self,
                 cluster_uuid=None,
                 resources=None,
                 node_selectors=None,
                 tensorflow=None,
                 horovod=None,
                 pytorch=None,
                 mxnet=None):
        self.cluster_uuid = cluster_uuid
        self.node_selectors = node_selectors
        self.resources = resources
        validate_frameworks([tensorflow, horovod, pytorch, mxnet])
        self.tensorflow = tensorflow
        self.horovod = horovod
        self.pytorch = pytorch
        self.mxnet = mxnet
