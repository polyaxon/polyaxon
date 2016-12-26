# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
import json
import os
import six
import yaml

from collections import Mapping

import numpy as np
import tensorflow as tf

from tensorflow.contrib.learn.python.learn.estimators import run_config

from polyaxon.libs.utils import generate_model_dir


def _maybe_load_json(item):
    """Parses `item` only if it is a string. If `item` is a dictionary it is returned as-is."""
    if isinstance(item, str):
        return json.loads(item)
    elif isinstance(item, dict):
        return item
    else:
        raise ValueError("Got {}, expected Json string or dict", type(item))


def _maybe_load_yaml(item):
    """Parses `item` only if it is a string. If `item` is a dictionary it is returned as-is."""
    if isinstance(item, str):
        return yaml.load(item)
    elif isinstance(item, dict):
        return item
    else:
        raise ValueError("Got {}, expected YAML string or dict", type(item))


@six.add_metaclass(abc.ABCMeta)
class Configurable(object):
    @classmethod
    def _read_configs(cls, config_values):
        if not isinstance(config_values, (np.ndarray, list, tuple)):
            config_values = [config_values]

        config = {}

        for config_value in config_values:
            if not isinstance(config_value, (Mapping, str)):
                raise 'Expects list of Mapping/string instances, received {} instead'.format(type(config_value))

            if isinstance(config_value, Mapping):
                config.update(config_value)
            else:
                config.update(cls._read_from_file(config_value))
        return config

    @classmethod
    def _read_from_file(cls, f_path):
        _, ext = os.path.splitext(f_path)
        if ext in ('.yml', '.yaml'):
            return cls._read_from_yml(f_path)
        elif ext == '.json':
            return cls._read_from_json(f_path)

    @staticmethod
    def _read_from_yml(f_path):
        with open(f_path) as f:
            f_config = yaml.safe_load(f)
            return f_config

    @staticmethod
    def _read_from_json(f_path):
        return json.loads(open(f_path).read())

    @classmethod
    def read_configs(cls, config_values):
        config = cls._read_configs(config_values)
        return cls(**config)


class PipelineConfig(Configurable):
    """The PipelineConfig holds information needed to create a `Pipeline`."""
    def __init__(self, name, dynamic_pad=True, bucket_boundaries=False, batch_size=64, num_epochs=4,
                 min_after_dequeue=5000, num_threads=3, shuffle=False, params=None):
        self.name = name
        self.dynamic_pad = dynamic_pad
        self.bucket_boundaries = bucket_boundaries
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.min_after_dequeue = min_after_dequeue
        self.num_threads = num_threads
        self.shuffle = shuffle
        self.params = params

    @property
    def capacity(self):
        return self.min_after_dequeue + self.num_threads * self.batch_size


class InputDataConfig(Configurable):
    """The InputDataConfig holds information needed to create a `InputData`."""
    NUMPY = 'NUMPY'
    PANDAS = 'PANDAS'

    def __init__(self, input_type=None, pipeline_config=None, x=None, y=None):
        self.input_type = input_type
        self.pipeline_config = pipeline_config
        self.x = x
        self.y = y

    @classmethod
    def read_configs(cls, config_values):
        config = cls._read_configs(config_values)

        config['pipeline_config'] = PipelineConfig.read_configs(config.get('pipeline_config'))

        return cls(**config)


class LossConfig(Configurable):
    """The LossConfig holds information needed to create a `Loss`."""
    def __init__(self, name, params=None):
        self.name = name
        self.params = params or {}


class MetricConfig(Configurable):
    """The MetricConfig holds information needed to create a `Metric`."""
    def __init__(self, name, params=None):
        self.name = name
        self.params = params or {}


class OptimizerConfig(Configurable):
    """The OptimizerConfig holds information needed to create a `Optimizer`."""
    def __init__(self, name, learning_rate=1e-4, lr_decay_type="", lr_decay_steps=100, lr_decay_rate=0.99,
                 lr_start_decay_at=0, lr_stop_decay_at=tf.int32.max, lr_min_learning_rate=1e-12, lr_staircase=False,
                 clip_gradients=5.0, sync_replicas=0, sync_replicas_to_aggregate=0, params=None):
        self.name = name
        self.learning_rate = learning_rate
        self.lr_decay_type = lr_decay_type
        self.lr_decay_steps = lr_decay_steps
        self.lr_decay_rate = lr_decay_rate
        self.lr_start_decay_at = lr_start_decay_at
        self.lr_stop_decay_at = lr_stop_decay_at
        self.lr_min_learning_rate = lr_min_learning_rate
        self.lr_staircase = lr_staircase
        self.clip_gradients = clip_gradients
        self.sync_replicas = sync_replicas
        self.sync_replicas_to_aggregate = sync_replicas_to_aggregate
        self.params = params or {}


class SubGraphConfig(Configurable):
    def __init__(self, name, methods, kwargs):
        self.name = name
        self.methods = methods
        self.kwargs = kwargs

    @classmethod
    def read_configs(cls, config_values):

        def add(method, m_kwargs):
            methods.append(method)
            if 'dependencies' in m_kwargs:
                m_kwargs['dependencies'] = [cls.__class__(**dependency) for dependency
                                            in m_kwargs['dependencies']]
            kwargs.append(m_kwargs)
            return methods, kwargs

        config = cls._read_configs(config_values)

        methods = []
        kwargs = []
        for (method, m_kwargs) in config.pop('definition', []):
                methods, kwargs = add(method, m_kwargs)

        config['methods'] = methods
        config['kwargs'] = kwargs

        return cls(**config)


class ModelConfig(Configurable):
    """The ModelConfig holds information needed to create a `Model`."""
    def __init__(self, loss_config, optimizer_config, graph_config, model_type, name='base_model',
                 eval_metrics_config=None, clip_gradients=5.0, params=None):
        self.name = name
        self.model_type = model_type
        self.loss_config = loss_config
        self.eval_metrics_config = eval_metrics_config
        self.optimizer_config = optimizer_config
        self.graph_config = graph_config
        self.clip_gradients = clip_gradients
        self.params = params or {}

    @classmethod
    def read_configs(cls, config_values):
        config = cls._read_configs(config_values)

        config['loss_config'] = LossConfig.read_configs(config['loss_config'])
        config['eval_metrics_config'] = [MetricConfig.read_configs(metric) for metric
                                         in config.get('eval_metrics_config', [])]
        config['optimizer_config'] = OptimizerConfig.read_configs(config['optimizer_config'])
        config['graph_config'] = SubGraphConfig.read_configs(config.get('graph_config'))

        return cls(**config)


class EstimatorConfig(Configurable):
    """The EstimatorConfig holds information needed to create a `Estimator`."""
    def __init__(self, name='estimator', output_dir=None, params=None):
        self.name = name
        self.output_dir = output_dir or generate_model_dir()
        self.params = params


def create_run_config(tf_random_seed=None, save_checkpoints_secs=None, save_checkpoints_steps=600,
                      keep_checkpoint_max=5, keep_checkpoint_every_n_hours=4, gpu_memory_fraction=1.0,
                      gpu_allow_growth=False, log_device_placement=False):
    config = run_config.RunConfig(
        tf_random_seed=tf_random_seed,
        save_checkpoints_secs=save_checkpoints_secs,
        save_checkpoints_steps=save_checkpoints_steps,
        keep_checkpoint_max=keep_checkpoint_max,
        keep_checkpoint_every_n_hours=keep_checkpoint_every_n_hours,
        gpu_memory_fraction=gpu_memory_fraction)
    config.tf_config.gpu_options.allow_growth = gpu_allow_growth
    config.tf_config.log_device_placement = log_device_placement
    return config


class ExperimentConfig(Configurable):
    """The ExperimentConfig holds information needed to create a `Experiment`."""
    def __init__(self, name, output_dir, run_config,
                 train_input_data_config, eval_input_data_config,
                 estimator_config, model_config, train_hooks_config=None, eval_hooks_config=None,
                 eval_metrics_config=None, eval_every_n_steps=1000, train_steps=10000,
                 eval_steps=100, eval_delay_secs=0, continuous_eval_throttle_secs=60,
                 delay_workers_by_global_step=False, export_strategies=None,
                 train_steps_per_iteration=1000):
        self.name = name
        self.output_dir = output_dir or "/tmp/polyaxon_logs/"

        self.run_config = run_config
        self.train_input_data_config = train_input_data_config
        self.eval_input_data_config = eval_input_data_config
        self.estimator_config = estimator_config
        self.model_config = model_config
        self.train_hooks_config = train_hooks_config or []
        self.eval_hooks_config = eval_hooks_config or []
        self.eval_metrics_config = eval_metrics_config or []
        self.eval_every_n_steps = eval_every_n_steps
        self.train_steps = train_steps
        self.eval_steps = eval_steps
        self.eval_delay_secs = eval_delay_secs
        self.continuous_eval_throttle_secs = continuous_eval_throttle_secs
        self.delay_workers_by_global_step = delay_workers_by_global_step
        self.export_strategies = export_strategies
        self.train_steps_per_iteration = train_steps_per_iteration

    @classmethod
    def read_configs(cls, config_values):
        config = cls._read_configs(config_values)

        config['run_config'] = create_run_config(**config.get('run_config', {}))
        config['train_input_data_config'] = InputDataConfig.read_configs(
            config['train_input_data_config'])
        config['eval_input_data_config'] = InputDataConfig.read_configs(
            config['eval_input_data_config'])
        config['estimator_config'] = EstimatorConfig.read_configs(config['estimator_config'])
        config['model_config'] = ModelConfig.read_configs(config['model_config'])

        return cls(**config)


SYNC_REPLICAS_OPTIMIZER = None
