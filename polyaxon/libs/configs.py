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


class RunConfig(run_config.RunConfig):
    def __init__(self, master=None, num_cores=0, log_device_placement=False,
                 gpu_memory_fraction=1.0, tf_random_seed=None, save_summary_steps=100,
                 save_checkpoints_secs=600, save_checkpoints_steps=None, keep_checkpoint_max=5,
                 keep_checkpoint_every_n_hours=10000, evaluation_master='', model_dir=None):
        super(RunConfig, self).__init__(master, num_cores, log_device_placement, gpu_memory_fraction,
                         tf_random_seed, save_summary_steps, save_checkpoints_secs,
                         save_checkpoints_steps, keep_checkpoint_max, keep_checkpoint_every_n_hours,
                         evaluation_master, model_dir)
        self._tf_random_seed = 1
        self._model_dir = None
        self._session_config = None

    @property
    def tf_random_seed(self):
        return self._tf_random_seed

    @property
    def model_dir(self):
        return self._model_dir

    @property
    def session_config(self):
        return self._session_config


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
    """`Configurable` is an abstract class for defining an configurable objects.

    A configurable class reads a configuration (YAML, Json) and create a config instance.
    """

    @classmethod
    def _read_configs(cls, config_values):
        if not isinstance(config_values, (np.ndarray, list, tuple)):
            config_values = [config_values]

        config = {}

        for config_value in config_values:
            if not isinstance(config_value, (Mapping, str)):
                raise TypeError('Expects list of Mapping/string instances, received {} instead'.format(type(config_value)))

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
        return cls(**config) if config else None


class PipelineConfig(Configurable):
    """The PipelineConfig holds information needed to create a `Pipeline`.

    Args:
        module: `str`, the pipeline module to use.
        name: `str`, name to give for the pipeline.
        dynamic_pad: `bool`, If True the piple uses dynamic padding.
        bucket_boundaries:
        batch_size: `int`, the batch size.
        num_epochs: number of epochs to iterate over in this pipeline.
        min_after_dequeue: `int`, number of element to have in the queue.
        num_threads: `int`, number of threads to use in the queue.
        shuffle: If true, shuffle the data.
        num_epochs: Number of times to iterate through the dataset. If None, iterate forever.
        params: `dict`, extra information to pass to the pipeline.
    """
    def __init__(self, module=None, name=None, subgraph_configs_by_features=None, dynamic_pad=True,
                 bucket_boundaries=False, batch_size=64, num_epochs=4,
                 min_after_dequeue=5000, num_threads=3, shuffle=False,
                 allow_smaller_final_batch=True, params=None):
        self.name = name
        self.module = module
        self.subgraph_configs_by_features = subgraph_configs_by_features
        self.dynamic_pad = dynamic_pad
        self.bucket_boundaries = bucket_boundaries
        self.batch_size = batch_size
        self.num_epochs = num_epochs
        self.min_after_dequeue = min_after_dequeue
        self.num_threads = num_threads
        self.shuffle = shuffle
        self.allow_smaller_final_batch = allow_smaller_final_batch
        self.params = params or {}

    @property
    def capacity(self):
        return self.min_after_dequeue + self.num_threads * self.batch_size

    @classmethod
    def read_configs(cls, config_values):
        config = cls._read_configs(config_values)
        subgraph_configs_by_features = {}
        for feature, subgraph_modules in config.pop('definition', {}).items():
            subgraph_config = {
                'name': '{}_processing'.format(feature),
                'definition': subgraph_modules
            }
            subgraph_configs_by_features[feature] = SubGraphConfig.read_configs(subgraph_config)

        config['subgraph_configs_by_features'] = subgraph_configs_by_features
        return cls(**config)


class InputDataConfig(Configurable):
    """The InputDataConfig holds information needed to create a `InputData`.

    Args:
        input_type: `str`, the type of the input data, e.g. numpy arrays.
        pipeline_config: The pipeline config to use.
        x: The x values, only used with NUMPY and PANDAS types.
        y: The y values, only used with NUMPY and PANDAS types.
    """
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
    """The LossConfig holds information needed to create a `Loss`.

    Args:
        module: `str`, module loss to use.
        params: `dict`, extra information to pass to the loss.
    """
    def __init__(self, module, params=None):
        self.module = module
        self.params = params or {}


class MetricConfig(Configurable):
    """The MetricConfig holds information needed to create a `Metric`.

    Args:
        module: `str`, name to give for the metric.
        params: `dict`, extra information to pass to the metric.
    """
    def __init__(self, module, params=None):
        self.module = module
        self.params = params or {}


class OptimizerConfig(Configurable):
    """The OptimizerConfig holds information needed to create a `Optimizer`.

    Args:
        module: `str`, optimizer optimizer to use.
        learning_rate: A Tensor or a floating point value. The learning rate to use.
        decay_steps: How often to apply decay.
        decay_rate: A Python number. The decay rate.
        start_decay_at: Don't decay before this step
        stop_decay_at: Don't decay after this step
        min_learning_rate: Don't decay below this number
        decay_type: A decay function name defined in `tf.train`
            possible Values: exponential_decay, inverse_time_decay, natural_exp_decay,
                             piecewise_constant, polynomial_decay.
        staircase: Whether to apply decay in a discrete staircase,
            as opposed to continuous, fashion.
        sync_replicas:
        sync_replicas_to_aggregate:
        params: `dict`, extra information to pass to the optimizer.
    """
    def __init__(self, module, learning_rate=1e-4, decay_type="", decay_steps=100,
                 decay_rate=0.99, start_decay_at=0, stop_decay_at=tf.int32.max,
                 min_learning_rate=1e-12, staircase=False, sync_replicas=0,
                 sync_replicas_to_aggregate=0, params=None):
        self.module = module
        self.learning_rate = learning_rate
        self.decay_type = decay_type
        self.decay_steps = decay_steps
        self.decay_rate = decay_rate
        self.start_decay_at = start_decay_at
        self.stop_decay_at = stop_decay_at
        self.min_learning_rate = min_learning_rate
        self.staircase = staircase
        self.sync_replicas = sync_replicas
        self.sync_replicas_to_aggregate = sync_replicas_to_aggregate
        self.params = params or {}


class SubGraphConfig(Configurable):
    """The configuration used to create subgraphs.

    Handles also nested subgraphs.

    Args:
        name: `str`. The name of this subgraph, used for creating the scope.
        modules: `list`.  The modules to connect inside this subgraph, e.g. layers
        features: `list`. The list of features to use for this subgraph.
        module: `str`. The Subgraph module to use. e.g.
    """
    def __init__(self, modules, kwargs, features=None, module=None, **params):
        self.modules = modules
        self.kwargs = kwargs
        self.features = features
        self.module = module
        self.params = params or {}

    @classmethod
    def read_configs(cls, config_values):

        def add(method, m_kwargs):
            modules.append(method)
            if 'modules' in m_kwargs:
                m_kwargs['modules'] = [cls.read_configs(module_config)
                                       for module_config in m_kwargs['modules']]
            kwargs.append(m_kwargs)
            return modules, kwargs

        config = cls._read_configs(config_values)
        if not config:
            return None

        modules = []
        kwargs = []
        for (method, m_kwargs) in config.pop('definition', []):
                modules, kwargs = add(method, m_kwargs)

        config['modules'] = modules
        config['kwargs'] = kwargs

        return cls(**config)


class BridgeConfig(Configurable):
    """The BridgeConfig class holds information neede to create a `Bridge` for a generator model.

    """
    def __init__(self, module, state_size=None, **params):
        self.module = module
        self.state_size = state_size
        self.params = params or {}


class ModelConfig(Configurable):
    """The ModelConfig holds information needed to create a `Model`.

    Args:
        loss_config: The loss configuration.
        optimizer_config: The optimizer configuration.
        graph_config: The graph configuration.
        model_type: `str`, The type of the model (`classifier`, 'regressor, or `generator`).
        summaries: `str` or `list`, the summary levels.
        eval_metrics_config: The evaluation metrics configuration.
        clip_gradients: `float`, The value to clip the gradients with.
        params: `dict`, extra information to pass to the model.
    """
    def __init__(self, loss_config, optimizer_config, module=None, graph_config=None,
                 encoder_config=None, decoder_config=None, bridge_config=None,
                 summaries='all', eval_metrics_config=None,
                 clip_gradients=5.0, **params):
        self.module = module
        self.summaries = summaries
        self.loss_config = loss_config
        self.eval_metrics_config = eval_metrics_config or []
        self.optimizer_config = optimizer_config
        self.graph_config = graph_config
        self.encoder_config = encoder_config
        self.decoder_config = decoder_config
        self.bridge_config = bridge_config
        self.clip_gradients = clip_gradients
        self.params = params or {}

    @classmethod
    def read_configs(cls, config_values):
        config = cls._read_configs(config_values)

        config['loss_config'] = LossConfig.read_configs(config.get('loss_config', {}))
        config['eval_metrics_config'] = [MetricConfig.read_configs(metric) for metric
                                         in config.get('eval_metrics_config', [])]
        config['optimizer_config'] = OptimizerConfig.read_configs(config.get('optimizer_config', {}))

        graph_config = config.get('graph_config', {})
        if graph_config:
            graph_config = [{'name': 'graph'}, graph_config]
        config['graph_config'] = SubGraphConfig.read_configs(graph_config)

        config['encoder_config'] = SubGraphConfig.read_configs(config.get('encoder_config', {}))
        config['decoder_config'] = SubGraphConfig.read_configs(config.get('decoder_config', {}))
        config['bridge_config'] = BridgeConfig.read_configs(config.get('bridge_config', {}))

        return cls(**config)


class EstimatorConfig(Configurable):
    """The EstimatorConfig holds information needed to create a `Estimator`.

    Args:
        cls: `str`, estimator class to use.
        output_dir: `str`, where to save training and evaluation data.
        params: `dict`, extra information to pass to the estimator.
    """
    def __init__(self, module='Estimator', output_dir=None, params=None):
        self.module = module
        self.output_dir = output_dir or generate_model_dir()
        self.params = params


def create_run_config(tf_random_seed=None, save_checkpoints_secs=None, save_checkpoints_steps=600,
                      keep_checkpoint_max=5, keep_checkpoint_every_n_hours=4,
                      gpu_memory_fraction=1.0, gpu_allow_growth=False, log_device_placement=False):
    """Creates a `RunConfig` instance."""
    config = RunConfig(
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
    """The ExperimentConfig holds information needed to create a `Experiment`.

    Args:
        name: `str`, name to give for the experiment.
        output_dir: `str`, where to save training and evaluation data.
        run_config: Tensorflow run config.
        train_input_data_config: Train input data configuration.
        eval_input_data_config: Eval input data configuration.
        estimator_config: The estimator configuration.
        model_config: The model configuration.
        train_hooks_config: The training hooks configuration.
        eval_hooks_config: The evaluation hooks configuration.
        eval_metrics_config: The evaluation metrics config.
        eval_every_n_steps: `int`, the frequency of evaluation.
        train_steps: `int`, the number of steps to train the model.
        eval_steps: `int`, the number of steps to eval the model.
        eval_delay_secs: `int`, used to delay the evaluation.
        continuous_eval_throttle_secs: Do not re-evaluate unless the last evaluation
            was started at least this many seconds ago for continuous_eval().
        delay_workers_by_global_step: if `True` delays training workers based on global step
            instead of time.
        export_strategies: A list of `ExportStrategy`s, or a single one, or None.
        train_steps_per_iteration: (applies only to continuous_train_and_evaluate).
    """
    def __init__(self, name, output_dir, run_config,
                 train_input_data_config, eval_input_data_config,
                 estimator_config, model_config, train_hooks_config=None, eval_hooks_config=None,
                 eval_metrics_config=None, eval_every_n_steps=1000, train_steps=10000,
                 eval_steps=10, eval_delay_secs=0, continuous_eval_throttle_secs=60,
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
