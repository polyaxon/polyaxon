# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import Schema, ValidationError, fields, post_load, validate

from polyaxon_schemas.base import BaseConfig
from polyaxon_schemas.logging import LoggingSchema, LoggingConfig


def validate_task(value):
    if 'type' not in value or value['type'] not in ClusterSchema.TYPES:
        raise ValidationError('Task type must be greater one of `{}`.'.format(ClusterSchema.TYPES))
    if 'index' not in value or not isinstance(value['index'], int):
        raise ValidationError('Task index must an intege.')


def validate_cluster(value):
    for key in value.keys():
        if key not in ClusterSchema.TYPES:
            raise ValidationError('`key` {} is not supported by ClusterConfig'.format(key))


class GPUOptionsSchema(Schema):
    gpu_memory_fraction = fields.Float(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return GPUOptionsConfig(**data)


class GPUOptionsConfig(BaseConfig):
    IDENTIFIER = 'session'
    SCHEMA = GPUOptionsSchema

    def __init__(self, gpu_memory_fraction=1.0):
        self.gpu_memory_fraction = gpu_memory_fraction


class SessionSchema(Schema):
    gpu_options = fields.Nested(GPUOptionsSchema, allow_none=True)
    log_device_placement = fields.Bool(allow_none=True)
    allow_soft_placement = fields.Float(allow_none=True)
    allow_growth = fields.Bool(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return SessionConfig(**data)


class SessionConfig(BaseConfig):
    IDENTIFIER = 'session'
    SCHEMA = SessionSchema

    def __init__(self,
                 log_device_placement=True,
                 gpu_options=GPUOptionsConfig(),
                 allow_soft_placement=True,
                 allow_growth=True):
        self.gpu_options = gpu_options
        self.log_device_placement = log_device_placement
        self.allow_soft_placement = allow_soft_placement
        self.allow_growth = allow_growth


class ClusterSchema(Schema):
    TYPES = ['master', 'ps', 'worker']

    environment = fields.String(allow_none=True)
    cluster = fields.Dict(validate=validate_cluster, allow_none=True)
    task = fields.Dict(validate=validate_task, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return ClusterConfig(**data)


class ClusterConfig(BaseConfig):
    IDENTIFIER = 'cluster'
    SCHEMA = ClusterSchema

    def __init__(self, environment=None, cluster=None, task=None):
        self.environment = environment
        self.cluster = cluster
        self.task = task


class RunSchema(Schema):
    model_dir = fields.String()
    tf_random_seed = fields.Int(allow_none=True)
    save_summary_steps = fields.Int(allow_none=True)
    save_checkpoints_secs = fields.Int(allow_none=True)
    save_checkpoints_steps = fields.Int(allow_none=True)
    keep_checkpoint_max = fields.Int(allow_none=True)
    keep_checkpoint_every_n_hours = fields.Int(allow_none=True)
    num_cores = fields.Int(allow_none=True)

    session_config = fields.Nested(SessionSchema, allow_none=True)
    cluster_config = fields.Nested(ClusterSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return RunConfig(**data)


class RunConfig(BaseConfig):
    IDENTIFIER = 'run'
    SCHEMA = RunSchema

    def __init__(self,
                 model_dir,
                 tf_random_seed=None,
                 save_summary_steps=100,
                 save_checkpoints_secs=None,
                 save_checkpoints_steps=None,
                 keep_checkpoint_max=5,
                 keep_checkpoint_every_n_hours=10000,
                 num_cores=None,
                 session_config=None,
                 cluster_config=None, ):
        self.model_dir = model_dir
        self.tf_random_seed = tf_random_seed
        self.save_summary_steps = save_summary_steps
        self.save_checkpoints_secs = save_checkpoints_secs
        self.save_checkpoints_steps = save_checkpoints_steps
        self.keep_checkpoint_max = keep_checkpoint_max
        self.keep_checkpoint_every_n_hours = keep_checkpoint_every_n_hours
        self.num_cores = num_cores
        self.session_config = session_config
        self.cluster_config = cluster_config


class EnvironmentSchema(Schema):
    type = fields.Str(allow_none=True, validate=validate.OneOf(['local', 'kubernetes']))
    distributed = fields.Bool(allow_none=True)
    n_workers = fields.Int(allow_none=True)
    n_ps = fields.Int(allow_none=True)
    delay_workers_by_global_step = fields.Bool(allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return EnvironmentConfig(**data)


class EnvironmentConfig(BaseConfig):
    SCHEMA = EnvironmentSchema
    IDENTIFIER = 'environment'

    def __init__(self,
                 type='local',  # pylint: disable=redefined-builtin
                 distributed=False,
                 n_workers=None,
                 n_ps=None,
                 delay_workers_by_global_step=False):
        self.type = type
        self.distributed = distributed
        self.n_workers = n_workers
        self.n_ps = n_ps
        self.delay_workers_by_global_step = delay_workers_by_global_step


class SettingsSchema(Schema):
    logging = fields.Nested(LoggingSchema, allow_none=True)
    train_strategy = fields.Str(allow_none=True)
    export_strategies = fields.Str(allow_none=True)
    environment = fields.Nested(EnvironmentSchema, allow_none=True)

    class Meta:
        ordered = True

    @post_load
    def make(self, data):
        return SettingsConfig(**data)


class SettingsConfig(BaseConfig):
    SCHEMA = SettingsSchema
    IDENTIFIER = 'settings'

    def __init__(self,
                 logging=LoggingConfig(),
                 train_strategy=None,
                 export_strategies=None,
                 environment=EnvironmentConfig()):
        self.logging = logging
        self.train_strategy = train_strategy
        self.export_strategies = export_strategies
        self.environment = environment
