# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import abc
import json
import os
import six
import yaml

from collections import Mapping, OrderedDict

import numpy as np
import tensorflow as tf

from tensorflow.contrib.learn.python.learn.estimators import run_config

from polyaxon.libs.exceptions import ConfigurationError
from polyaxon.libs.utils import generate_model_dir


@six.add_metaclass(abc.ABCMeta)
class Configurable(object):
    """`Configurable` is an abstract class for defining an configurable objects.

    A configurable class reads a configuration (YAML, Json) and create a config instance.
    """

    @classmethod
    def _read_configs(cls, config_values):
        if not isinstance(config_values, (np.ndarray, list, tuple)):
            config_values = [config_values]

        if not config_values:
            return None

        config = {}
        for config_value in config_values:
            if not isinstance(config_value, (Mapping, six.string_types)):
                raise ConfigurationError(
                    'Expects list of Mapping/string instances, '
                    'received {} instead'.format(type(config_value)))

            if isinstance(config_value, Mapping):
                config.update(config_value)
            elif os.path.isfile(config_value):
                config.update(cls._read_from_file(config_value))
            else:
                raise ConfigurationError(
                    "The provided value could not be parsed, please provide a valid: "
                    "Python dict or path to a configuration file."
                )
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

    def to_dict(self):
        raise NotImplementedError


class RunConfig(run_config.RunConfig, Configurable):
    def __init__(self,
                 master=None,
                 num_cores=0,
                 log_device_placement=False,
                 gpu_memory_fraction=1.0,
                 tf_random_seed=None,
                 save_summary_steps=100,
                 save_checkpoints_secs=600,
                 save_checkpoints_steps=None,
                 keep_checkpoint_max=5,
                 keep_checkpoint_every_n_hours=10000,
                 evaluation_master='',
                 model_dir=None,
                 cluster_config=None):
        self.create_cluster_config(cluster_config)
        if save_checkpoints_steps is not None:
            save_checkpoints_secs = None
        super(RunConfig, self).__init__(master, num_cores, log_device_placement,
                                        gpu_memory_fraction,
                                        tf_random_seed, save_summary_steps, save_checkpoints_secs,
                                        save_checkpoints_steps, keep_checkpoint_max,
                                        keep_checkpoint_every_n_hours,
                                        evaluation_master, model_dir)
        self._tf_random_seed = 1
        self._model_dir = None
        self._session_config = None
        self._to_dict = OrderedDict([
            ('master', master),
            ('num_cores', num_cores),
            ('log_device_placement', log_device_placement),
            ('gpu_memory_fraction', gpu_memory_fraction),
            ('tf_random_seed', tf_random_seed),
            ('save_summary_steps', save_summary_steps),
            ('save_checkpoints_secs', save_checkpoints_secs),
            ('save_checkpoints_steps', save_checkpoints_steps),
            ('keep_checkpoint_max', keep_checkpoint_max),
            ('keep_checkpoint_every_n_hours', keep_checkpoint_every_n_hours),
            ('evaluation_master', evaluation_master),
            ('model_dir', model_dir),
            ('cluster_config', cluster_config)
        ])

    @property
    def tf_random_seed(self):
        return self._tf_random_seed

    @property
    def model_dir(self):
        return self._model_dir

    @property
    def session_config(self):
        return self._session_config

    def to_dict(self):
        return self._to_dict

    @classmethod
    def read_configs(cls, config_values):
        config_values = cls._read_configs(config_values)
        gpu_allow_growth = config_values.pop('gpu_allow_growth', False)
        log_device_placement = config_values.pop('log_device_placement', False)
        config = cls(**config_values)
        config.tf_config.gpu_options.allow_growth = gpu_allow_growth
        config.tf_config.log_device_placement = log_device_placement
        return config

    @staticmethod
    def create_cluster_config(cluster_config):
        """Sets the cluster config to the environment variable `TF_CONFIG`.

        Args:
            cluster_config: `dict`. Represents the cluster config dictionary.
        """
        # First we need to check the type of the task for this env
        task_type = os.environ.get('task_type')
        if task_type not in ['master', 'ps', 'worker']:
            return

        try:
            task_id = int(os.environ.get('task_index'))
        except TypeError:
            return

        config = {
            'environment': cluster_config.pop('environment', 'cloud'),
            'cluster': cluster_config,
            'task': {'type': task_type, 'index': task_id}
        }
        # Set the cluster config in the environment variable `TF_CONFIG`.
        os.environ['TF_CONFIG'] = json.dumps(config)


class PipelineConfig(Configurable):
    """The PipelineConfig holds information needed to create a `Pipeline`.

    Args:
        module: `str`, the pipeline module to use.
        name: `str`, name to give for the pipeline.
        dynamic_pad: `bool`, If True the pipleine uses dynamic padding.
        bucket_boundaries:
        batch_size: `int`, the batch size.
        num_epochs: number of epochs to iterate over in this pipeline.
        min_after_dequeue: `int`, number of element to have in the queue.
        num_threads: `int`, number of threads to use in the queue.
        shuffle: If true, shuffle the data.
        num_epochs: Number of times to iterate through the dataset. If None, iterate forever.
        params: `dict`, extra information to pass to the pipeline.
    """

    def __init__(self,
                 module=None,
                 name=None,
                 subgraph_configs_by_features=None,
                 dynamic_pad=True,
                 bucket_boundaries=False,
                 batch_size=64,
                 num_epochs=1,
                 min_after_dequeue=5000,
                 num_threads=3,
                 shuffle=False,
                 allow_smaller_final_batch=True,
                 params=None):
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

    def to_dict(self):
        def module_to_dict(feature, subgraph):
            if '_processing' in feature:
                feature = feature.split('_processing')[0]
            return feature, subgraph.to_dict()['definition']

        return OrderedDict([
            ('name', self.name),
            ('module', self.module),
            ('definition', OrderedDict(
                [module_to_dict(feature, self.subgraph_configs_by_features[feature])
                 for feature in self.subgraph_configs_by_features])),
            ('dynamic_pad', self.dynamic_pad),
            ('bucket_boundaries', self.bucket_boundaries),
            ('batch_size', self.batch_size),
            ('num_epochs', self.num_epochs),
            ('min_after_dequeue', self.min_after_dequeue),
            ('num_threads', self.num_threads),
            ('shuffle', self.shuffle),
            ('allow_smaller_final_batch', self.allow_smaller_final_batch),
            ('params', self.params),
        ])


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

    def to_dict(self):
        return OrderedDict([
            ('input_type', self.input_type),
            ('pipeline_config', self.pipeline_config.to_dict()),
            ('x', self.x),
            ('y', self.y)
        ])


class EnvironmentConfig(Configurable):
    """The EnvironmentConfig holds information needed to create an `Environment`.

    Args:
        module: `str`, module loss to use.
        params: `dict`, extra information to pass to the loss.
    """

    def __init__(self, module, env_id, params=None):
        self.module = module
        self.env_id = env_id
        self.params = params or {}

    def to_dict(self):
        return OrderedDict([
            ('module', self.module),
            ('env_id', self.env_id),
            ('params', self.params),
        ])


class LossConfig(Configurable):
    """The LossConfig holds information needed to create a `Loss`.

    Args:
        module: `str`, module loss to use.
        params: `dict`, extra information to pass to the loss.
    """

    def __init__(self, module, params=None):
        self.module = module
        self.params = params or {}

    def to_dict(self):
        return OrderedDict([
            ('module', self.module),
            ('params', self.params),
        ])


class MetricConfig(Configurable):
    """The MetricConfig holds information needed to create a `Metric`.

    Args:
        module: `str`, name to give for the metric.
        params: `dict`, extra information to pass to the metric.
    """

    def __init__(self, module, params=None):
        self.module = module
        self.params = params or {}

    def to_dict(self):
        return OrderedDict([
            ('module', self.module),
            ('params', self.params),
        ])


class ExplorationConfig(Configurable):
    """The ExplorationConfig holds information needed to create a `Exploration`.

    Args:
        module: `str`, name to give for the exploration.
        params: `dict`, extra information to pass to the exploration.
    """

    def __init__(self, module, params=None):
        self.module = module
        self.params = params or {}

    def to_dict(self):
        return OrderedDict([
            ('module', self.module),
            ('params', self.params),
        ])


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

    def __init__(self,
                 module,
                 learning_rate=1e-4,
                 decay_type="",
                 decay_steps=10000,
                 decay_rate=0.99,
                 start_decay_at=0,
                 stop_decay_at=tf.int32.max,
                 min_learning_rate=1e-12,
                 staircase=False,
                 sync_replicas=0,
                 sync_replicas_to_aggregate=0,
                 params=None):
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

    def to_dict(self):
        return OrderedDict([
            ('module', self.module),
            ('learning_rate', self.learning_rate),
            ('decay_type', self.decay_type),
            ('decay_steps', self.decay_steps),
            ('decay_rate', self.decay_rate),
            ('start_decay_at', self.start_decay_at),
            ('stop_decay_at', self.stop_decay_at),
            ('min_learning_rate', self.min_learning_rate),
            ('staircase', self.staircase),
            ('sync_replicas', self.sync_replicas),
            ('sync_replicas_to_aggregate', self.sync_replicas_to_aggregate),
            ('params', self.params),
        ])


class MemoryConfig(Configurable):
    """The MemoryConfig holds information needed to create a `Memory` for an agent.

    Args:
        module: `str`, name to give for the memory.
        params: `dict`, extra information to pass to the memory.
    """

    def __init__(self, module, params=None):
        self.module = module
        self.params = params or {}

    def to_dict(self):
        return OrderedDict([
            ('module', self.module),
            ('params', self.params),
        ])


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

    def to_dict(self):
        def module_to_dict(module, m_kwargs):
            if 'modules' in m_kwargs:
                m_kwargs['modules'] = [m.to_dict() for m in m_kwargs['modules']]
            return module, m_kwargs

        d = OrderedDict([
            ('module', self.module),
            ('definition', [module_to_dict(m, k) for m, k in zip(self.modules, self.kwargs)]),
        ])
        d.update(self.params)
        return d


class BridgeConfig(Configurable):
    """The BridgeConfig class holds information neede to create a `Bridge` for a generator model.

    """

    def __init__(self, module, state_size=None, **params):
        self.module = module
        self.state_size = state_size
        self.params = params or {}

    def to_dict(self):
        return OrderedDict([
            ('module', self.module),
            ('state_size', self.state_size),
            ('params', self.params)
        ])


class ModelConfig(Configurable):
    """The ModelConfig holds information needed to create a `Model`.

    Args:
        loss_config: The loss configuration.
        optimizer_config: The optimizer configuration.
        graph_config: The graph configuration.
        module: `str`, The type of the model (`classifier`, 'regressor, or `generator`).
        summaries: `str` or `list`, the summary levels.
        eval_metrics_config: The evaluation metrics configuration.
        clip_gradients: `float`, The value to clip the gradients with.
        params: `dict`, extra information to pass to the model.
    """

    def __init__(self,
                 loss_config=None,
                 optimizer_config=None,
                 module=None,
                 graph_config=None,
                 encoder_config=None,
                 decoder_config=None,
                 bridge_config=None,
                 summaries='all',
                 eval_metrics_config=None,
                 clip_gradients=5.0,
                 clip_embed_gradients=0.1,
                 **params):
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
        self.clip_embed_gradients = clip_embed_gradients
        self.params = params or {}

    @classmethod
    def read_configs(cls, config_values):
        config = cls._read_configs(config_values)

        config['loss_config'] = LossConfig.read_configs(config.get('loss_config', {}))
        config['eval_metrics_config'] = [MetricConfig.read_configs(metric) for metric
                                         in config.get('eval_metrics_config', [])]
        config['optimizer_config'] = OptimizerConfig.read_configs(
            config.get('optimizer_config', {}))

        graph_config = config.get('graph_config', {})
        if graph_config:
            graph_config = [{'name': 'graph'}, graph_config]
        config['graph_config'] = SubGraphConfig.read_configs(graph_config)

        config['encoder_config'] = SubGraphConfig.read_configs(config.get('encoder_config', {}))
        config['decoder_config'] = SubGraphConfig.read_configs(config.get('decoder_config', {}))
        config['bridge_config'] = BridgeConfig.read_configs(config.get('bridge_config', {}))

        return cls(**config)

    def to_dict(self):
        d = OrderedDict([
            ('module', self.module),
            ('summaries', self.summaries),
            ('loss_config', self.loss_config.to_dict() if self.loss_config else None),
            ('eval_metrics_config', [m.to_dict() for m in self.eval_metrics_config]),
            ('optimizer_config', self.optimizer_config.to_dict()),
            ('graph_config', self.graph_config.to_dict() if self.graph_config else None),
            ('encoder_config', self.encoder_config.to_dict() if self.encoder_config else None),
            ('decoder_config', self.decoder_config.to_dict() if self.decoder_config else None),
            ('bridge_config', self.bridge_config.to_dict() if self.bridge_config else None),
            ('clip_gradients', self.clip_gradients),
            ('clip_embed_gradients', self.clip_embed_gradients),
        ])

        d.update(**self.params)
        return d


class EstimatorConfig(Configurable):
    """The EstimatorConfig holds information needed to create a `Estimator`.

    Args:
        module: `str`, estimator class to use.
        output_dir: `str`, where to save training and evaluation data.
        params: `dict`, extra information to pass to the estimator.
    """

    def __init__(self, module='Estimator', output_dir=None, params=None):
        self.module = module
        self.output_dir = output_dir or generate_model_dir()
        self.params = params

    def to_dict(self):
        return OrderedDict([
            ('module', self.module),
            ('output_dir', self.output_dir),
            ('params', self.params),
        ])


class AgentConfig(EstimatorConfig):
    """The EstimatorConfig holds information needed to create a `Estimator`.

    Args:
        module: `str`, estimator class to use.
        output_dir: `str`, where to save training and evaluation data.
        params: `dict`, extra information to pass to the estimator.
    """

    def __init__(self, module='Agent', memory_config=None, output_dir=None, params=None):
        self.memory_config = memory_config or None
        super(AgentConfig, self).__init__(module=module, output_dir=output_dir, params=params)

    def to_dict(self):
        d = super(AgentConfig, self).to_dict()
        d.update({'memory_config': self.memory_config.to_dict()})
        return d

    @classmethod
    def read_configs(cls, config_values):
        config = cls._read_configs(config_values)
        config['memory_config'] = MemoryConfig.read_configs(config['memory_config'])

        return cls(**config)


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

    def __init__(self,
                 name,
                 output_dir,
                 run_config,
                 train_input_data_config,
                 eval_input_data_config,
                 estimator_config,
                 model_config,
                 train_hooks_config=None,
                 eval_hooks_config=None,
                 eval_metrics_config=None,
                 eval_every_n_steps=1000,
                 train_steps=10000,
                 eval_steps=10,
                 eval_delay_secs=0,
                 continuous_eval_throttle_secs=60,
                 delay_workers_by_global_step=False,
                 export_strategies=None,
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

        config['run_config'] = RunConfig.read_configs(config.get('run_config', {}))
        config['train_input_data_config'] = InputDataConfig.read_configs(
            config['train_input_data_config'])
        config['eval_input_data_config'] = InputDataConfig.read_configs(
            config['eval_input_data_config'])
        config['estimator_config'] = EstimatorConfig.read_configs(config['estimator_config'])
        config['model_config'] = ModelConfig.read_configs(config['model_config'])

        return cls(**config)

    def to_dict(self):
        return OrderedDict([
            ('name', self.name),
            ('output_dir', self.output_dir),
            ('run_config', self.run_config.to_dict()),
            ('train_input_data_config', self.train_input_data_config.to_dict()),
            ('eval_input_data_config', self.eval_input_data_config.to_dict()),
            ('estimator_config', self.estimator_config.to_dict()),
            ('model_config', self.model_config.to_dict()),
            ('train_hooks_config', self.train_hooks_config),
            ('eval_hooks_config', self.eval_hooks_config),
            ('eval_metrics_config', self.eval_metrics_config),
            ('eval_every_n_steps', self.eval_every_n_steps),
            ('train_steps', self.train_steps),
            ('eval_steps', self.eval_steps),
            ('eval_delay_secs', self.eval_delay_secs),
            ('continuous_eval_throttle_secs', self.continuous_eval_throttle_secs),
            ('delay_workers_by_global_step', self.delay_workers_by_global_step),
            ('export_strategies', self.export_strategies),
            ('train_steps_per_iteration', self.train_steps_per_iteration),
        ])


class RLExperimentConfig(Configurable):
    """The RLExperimentConfig holds information needed to create a `RLExperiment`.

    Args:
        name: `str`, name to give for the experiment.
        output_dir: `str`, where to save training and evaluation data.
        run_config: Tensorflow run config.
        environment_config: Eval environment configuration.
        run_config: The agent configuration.
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

    def __init__(self,
                 name,
                 output_dir,
                 run_config,
                 environment_config,
                 agent_config,
                 model_config,
                 train_hooks_config=None,
                 eval_hooks_config=None,
                 eval_metrics_config=None,
                 eval_every_n_steps=1000,
                 train_steps=10000,
                 train_episodes=100,
                 first_update=5000,
                 update_frequency=15,
                 eval_steps=10,
                 eval_delay_secs=0,
                 continuous_eval_throttle_secs=60,
                 delay_workers_by_global_step=False,
                 export_strategies=None,
                 train_steps_per_iteration=1000):
        self.name = name
        self.output_dir = output_dir or "/tmp/polyaxon_logs/"

        self.run_config = run_config
        self.environment_config = environment_config
        self.agent_config = agent_config
        self.model_config = model_config
        self.train_hooks_config = train_hooks_config or []
        self.eval_hooks_config = eval_hooks_config or []
        self.eval_metrics_config = eval_metrics_config or []
        self.eval_every_n_steps = eval_every_n_steps
        self.train_steps = train_steps
        self.train_episodes = train_episodes
        self.first_update = first_update
        self.update_frequency = update_frequency
        self.eval_steps = eval_steps
        self.eval_delay_secs = eval_delay_secs
        self.continuous_eval_throttle_secs = continuous_eval_throttle_secs
        self.delay_workers_by_global_step = delay_workers_by_global_step
        self.export_strategies = export_strategies
        self.train_steps_per_iteration = train_steps_per_iteration

    @classmethod
    def read_configs(cls, config_values):
        config = cls._read_configs(config_values)

        config['run_config'] = RunConfig.read_configs(config.get('run_config', {}))
        config['environment_config'] = EnvironmentConfig.read_configs(config['environment_config'])
        config['agent_config'] = AgentConfig.read_configs(config['agent_config'])
        config['model_config'] = ModelConfig.read_configs(config['model_config'])

        return cls(**config)

    def to_dict(self):
        return OrderedDict([
            ('name', self.name),
            ('output_dir', self.output_dir),
            ('run_config', self.run_config.to_dict()),
            ('environment_config', self.environment_config.to_dict()),
            ('agent_config', self.agent_config.to_dict()),
            ('model_config', self.model_config.to_dict()),
            ('train_hooks_config', self.train_hooks_config),
            ('eval_hooks_config', self.eval_hooks_config),
            ('eval_metrics_config', self.eval_metrics_config),
            ('eval_every_n_steps', self.eval_every_n_steps),
            ('train_steps', self.train_steps),
            ('train_episodes', self.train_episodes),
            ('first_update', self.first_update),
            ('update_frequency', self.update_frequency),
            ('eval_steps', self.eval_steps),
            ('eval_delay_secs', self.eval_delay_secs),
            ('continuous_eval_throttle_secs', self.continuous_eval_throttle_secs),
            ('delay_workers_by_global_step', self.delay_workers_by_global_step),
            ('export_strategies', self.export_strategies),
            ('train_steps_per_iteration', self.train_steps_per_iteration),
        ])


SYNC_REPLICAS_OPTIMIZER = None
