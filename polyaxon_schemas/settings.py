# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, fields, post_load, validate, post_dump

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.logging import LoggingSchema, LoggingConfig
from polyaxon_schemas.utils import RunTypes, UUID, SEARCH_METHODS


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
            self.cpu = other.cpu

        if self.memory:
            if other.memory:
                self.memory += other.memory
        elif other.memory:
            self.memory = other.memory

        if self.gpu:
            if other.gpu:
                self.gpu += other.gpu
        elif other.gpu:
            self.gpu = other.gpu
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


class ClusterSchema(Schema):
    master = fields.List(fields.Str(), allow_none=True)
    worker = fields.List(fields.Str(), allow_none=True)
    ps = fields.List(fields.Str(), allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ClusterConfig(**data)

    @post_dump
    def unmake(self, data):
        return ClusterConfig.remove_reduced_attrs(data)


class ClusterConfig(BaseConfig):
    """Tensorfow cluster definition"""
    IDENTIFIER = 'cluster'
    SCHEMA = ClusterSchema

    def __init__(self, master=None, worker=None, ps=None):
        self.master = master
        self.worker = worker
        self.ps = ps


class RunSchema(Schema):
    tf_random_seed = fields.Int(allow_none=True)
    save_summary_steps = fields.Int(allow_none=True)
    save_checkpoints_secs = fields.Int(allow_none=True)
    save_checkpoints_steps = fields.Int(allow_none=True)
    keep_checkpoint_max = fields.Int(allow_none=True)
    keep_checkpoint_every_n_hours = fields.Int(allow_none=True)

    session = fields.Nested(SessionSchema, allow_none=True)
    cluster = fields.Nested(ClusterSchema, allow_none=True)

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


class EnvironmentSchema(Schema):
    cluster_uuid = UUID(allow_none=True)
    n_workers = fields.Int(allow_none=True)
    n_ps = fields.Int(allow_none=True)
    delay_workers_by_global_step = fields.Bool(allow_none=True)
    run_config = fields.Nested(RunSchema, allow_none=True)
    resources = fields.Nested(PodResourcesSchema, allow_none=True)
    default_worker_config = fields.Nested(SessionSchema, allow_none=True)
    default_worker_resources = fields.Nested(PodResourcesSchema, allow_none=True)
    default_ps_config = fields.Nested(SessionSchema, allow_none=True)
    default_ps_resources = fields.Nested(PodResourcesSchema, allow_none=True)
    worker_configs = fields.Nested(SessionSchema, many=True, allow_none=True)
    worker_resources = fields.Nested(PodResourcesSchema, many=True, allow_none=True)
    ps_configs = fields.Nested(SessionSchema, many=True, allow_none=True)
    ps_resources = fields.Nested(PodResourcesSchema, many=True, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return EnvironmentConfig(**data)

    @post_dump
    def unmake(self, data):
        return EnvironmentConfig.remove_reduced_attrs(data)


class EnvironmentConfig(BaseConfig):
    IDENTIFIER = 'environment'
    SCHEMA = EnvironmentSchema

    def __init__(self,
                 cluster_uuid=None,
                 n_workers=0,
                 n_ps=0,
                 delay_workers_by_global_step=False,
                 run_config=None,
                 resources=None,
                 default_worker_config=None,
                 default_worker_resources=None,
                 default_ps_config=None,
                 default_ps_resources=None,
                 worker_configs=None,
                 worker_resources=None,
                 ps_configs=None,
                 ps_resources=None):
        self.cluster_uuid = cluster_uuid
        self.n_workers = n_workers
        self.n_ps = n_ps
        self.delay_workers_by_global_step = delay_workers_by_global_step
        self.run_config = run_config
        self.resources = resources
        self.default_worker_config = default_worker_config
        self.default_worker_resources = default_worker_resources
        self.default_ps_config = default_ps_config
        self.default_ps_resources = default_ps_resources
        self.worker_configs = worker_configs
        self.worker_resources = worker_resources
        self.ps_configs = ps_configs
        self.ps_resources = ps_resources


class EarlyStoppingMetricSchema(Schema):
    metric = fields.Str()
    value = fields.Float()
    higher = fields.Bool(default=True, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return EarlyStoppingMetricConfig(**data)

    @post_dump
    def unmake(self, data):
        return EarlyStoppingMetricConfig.remove_reduced_attrs(data)


class EarlyStoppingMetricConfig(BaseConfig):
    SCHEMA = EarlyStoppingMetricSchema
    IDENTIFIER = 'early_stopping_metric'

    def __init__(self,
                 metric,
                 value=None,
                 higher=True):
        self.metric = metric
        self.value = value
        self.higher = higher


class SettingsSchema(Schema):
    logging = fields.Nested(LoggingSchema, allow_none=True)
    export_strategies = fields.Str(allow_none=True)
    run_type = fields.Str(allow_none=True, validate=validate.OneOf(RunTypes.VALUES))
    concurrent_experiments = fields.Int(allow_none=True)
    search_method = fields.Str(allow_none=True, validate=validate.OneOf(SEARCH_METHODS.VALUES))
    n_experiments = fields.Int(allow_none=True)
    early_stopping = fields.Nested(EarlyStoppingMetricSchema, many=True, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return SettingsConfig(**data)

    @post_dump
    def unmake(self, data):
        return SettingsConfig.remove_reduced_attrs(data)


class SettingsConfig(BaseConfig):
    SCHEMA = SettingsSchema
    IDENTIFIER = 'settings'

    def __init__(self,
                 logging=LoggingConfig(),
                 export_strategies=None,
                 run_type=RunTypes.KUBERNETES,
                 concurrent_experiments=1,
                 search_method=SEARCH_METHODS.SEQUENTIAL,
                 n_experiments=None,
                 early_stopping=None):
        self.logging = logging
        self.export_strategies = export_strategies
        self.run_type = run_type
        self.concurrent_experiments = concurrent_experiments
        self.search_method = search_method
        self.n_experiments = n_experiments
        self.early_stopping = early_stopping
