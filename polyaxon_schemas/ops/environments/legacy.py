# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields

from polyaxon_schemas.base import BaseConfig, BaseSchema
from polyaxon_schemas.ops.environments.pods import EnvironmentConfig, EnvironmentSchema
from polyaxon_schemas.ops.experiment.environment import TensorflowClusterSchema


class GPUOptionsSchema(BaseSchema):
    gpu_memory_fraction = fields.Float(allow_none=True)
    allow_growth = fields.Bool(allow_none=True)
    per_process_gpu_memory_fraction = fields.Float(allow_none=True)

    @staticmethod
    def schema_config():
        return GPUOptionsConfig


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


class SessionSchema(BaseSchema):
    gpu_options = fields.Nested(GPUOptionsSchema, allow_none=True)
    log_device_placement = fields.Bool(allow_none=True)
    allow_soft_placement = fields.Bool(allow_none=True)
    intra_op_parallelism_threads = fields.Int(allow_none=True)
    inter_op_parallelism_threads = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return SessionConfig


class SessionConfig(BaseConfig):
    IDENTIFIER = 'session'
    SCHEMA = SessionSchema

    def __init__(self,
                 log_device_placement=True,
                 gpu_options=GPUOptionsConfig(),
                 allow_soft_placement=True,
                 intra_op_parallelism_threads=None,
                 inter_op_parallelism_threads=None):
        self.gpu_options = gpu_options
        self.log_device_placement = log_device_placement
        self.allow_soft_placement = allow_soft_placement
        self.intra_op_parallelism_threads = intra_op_parallelism_threads
        self.inter_op_parallelism_threads = inter_op_parallelism_threads


class TFRunSchema(BaseSchema):
    tf_random_seed = fields.Int(allow_none=True)
    save_summary_steps = fields.Int(allow_none=True)
    save_checkpoints_secs = fields.Int(allow_none=True)
    save_checkpoints_steps = fields.Int(allow_none=True)
    keep_checkpoint_max = fields.Int(allow_none=True)
    keep_checkpoint_every_n_hours = fields.Int(allow_none=True)

    session = fields.Nested(SessionSchema, allow_none=True)
    cluster = fields.Nested(TensorflowClusterSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return TFRunConfig


class TFRunConfig(BaseConfig):
    IDENTIFIER = 'run'
    SCHEMA = TFRunSchema

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


class TensorflowPodEnvironmentSchema(EnvironmentSchema):
    config = fields.Nested(SessionSchema, allow_none=True)

    @staticmethod
    def schema_config():
        return TensorflowPodEnvironmentConfig


class TensorflowPodEnvironmentConfig(EnvironmentConfig):
    IDENTIFIER = 'pod_environment'
    SCHEMA = TensorflowPodEnvironmentSchema
    REDUCED_ATTRIBUTES = EnvironmentConfig.REDUCED_ATTRIBUTES + ['config']

    def __init__(self,
                 index=None,
                 config=None,
                 resources=None,
                 node_selector=None,
                 affinity=None,
                 tolerations=None,
                 ):
        self.config = config
        super(TensorflowPodEnvironmentConfig, self).__init__(
            index=index,
            resources=resources,
            node_selector=node_selector,
            affinity=affinity,
            tolerations=tolerations,
        )
