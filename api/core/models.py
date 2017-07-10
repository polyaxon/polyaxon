# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import json

import polyaxon as plx
import tensorflow as tf

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models

from polyaxon.estimators.hooks import HOOKS
from polyaxon.models.summarizer import SummaryOptions

from core.utils import remove_empty_keys
from libs.models import DiffModel


class Loss(DiffModel):
    LOSSES = ((obj, obj) for obj in plx.losses.LOSSES.keys())

    module = models.CharField(max_length=256, choices=LOSSES)
    params = JSONField(blank=True, null=True, default={})

    def __str__(self):
        return '{}-{}'.format(self.module, self.id)

    def to_dict(self):
        return {'module': self.module, 'params': self.params}

    @staticmethod
    def from_config(config):
        if not config:
            return None
        config_dict = config.to_dict()
        config_dict = remove_empty_keys(config_dict)
        return Loss.objects.create(**config_dict)

    def to_config(self):
        return plx.configs.LossConfig(**self.to_dict())


class Metric(DiffModel):
    METRICS = ((obj, obj) for obj in plx.metrics.EVAL_METRICS.keys())

    module = models.CharField(max_length=256, choices=METRICS)
    params = JSONField(blank=True, null=True, default={})

    def __str__(self):
        return '{}-{}'.format(self.module, self.id)

    def to_dict(self):
        return {'module': self.module, 'params': self.params}

    @staticmethod
    def from_config(config):
        if not config:
            return None

        config_dict = config.to_dict()
        config_dict = remove_empty_keys(config_dict)
        return Metric.objects.create(**config_dict)

    def to_config(self):
        return plx.configs.MetricConfig(**self.to_dict())


class AgentMemory(DiffModel):
    MEMORIES = ((obj, obj) for obj in plx.rl.memories.MEMORIES.keys())

    module = models.CharField(max_length=256, choices=MEMORIES)
    params = JSONField(blank=True, null=True, default={})

    def __str__(self):
        return '{}-{}'.format(self.module, self.id)

    def to_dict(self):
        return {'module': self.module, 'params': self.params}

    @staticmethod
    def from_config(config):
        if not config:
            return None

        config_dict = config.to_dict()
        config_dict = remove_empty_keys(config_dict)
        return AgentMemory.objects.create(**config_dict)

    def to_config(self):
        return plx.configs.MetricConfig(**self.to_dict())


class Optimizer(DiffModel):
    OPTIMIZERS = ((obj, obj) for obj in plx.optimizers.OPTIMIZERS.keys())

    module = models.CharField(max_length=256, choices=OPTIMIZERS)
    learning_rate = models.FloatField(default=1e-4)
    decay_type = models.CharField(max_length=256, null=True, blank=True, default="")
    decay_steps = models.IntegerField(default=100)
    decay_rate = models.FloatField(default=0.99)
    start_decay_at = models.IntegerField(default=0)
    stop_decay_at = models.IntegerField(default=tf.int32.max)
    min_learning_rate = models.FloatField(default=1e-12)
    staircase = models.BooleanField(default=False)
    sync_replicas = models.IntegerField(default=0)
    sync_replicas_to_aggregate = models.IntegerField(default=0)
    params = JSONField(blank=True, null=True, default={})

    def __str__(self):
        return '{}-{}'.format(self.module, self.id)

    def to_dict(self):
        return {
            'module': self.module,
            'learning_rate': self.learning_rate,
            'decay_type': self.decay_type,
            'decay_steps': self.decay_steps,
            'decay_rate': self.decay_rate,
            'start_decay_at': self.start_decay_at,
            'stop_decay_at': self.stop_decay_at,
            'min_learning_rate': self.min_learning_rate,
            'staircase': self.staircase,
            'sync_replicas': self.sync_replicas,
            'sync_replicas_to_aggregate': self.sync_replicas_to_aggregate,
            'params': self.params
        }

    @staticmethod
    def from_config(config):
        if not config:
            return None

        config_dict = config.to_dict()
        config_dict = remove_empty_keys(config_dict)
        return Optimizer.objects.create(**config_dict)

    def to_config(self):
        return plx.configs.OptimizerConfig(**self.to_dict())


class Bridge(DiffModel):
    BRIDGES = ((obj, obj) for obj in plx.bridges.BRIDGES.keys())

    module = models.CharField(max_length=256, choices=BRIDGES)
    state_size = models.CharField(max_length=64, null=True, blank=True)
    params = JSONField(blank=True, null=True, default={})

    def __str__(self):
        return '{}-{}'.format(self.module, self.id)

    def to_dict(self):
        return {
            'module': self.module,
            'state_size': self.state_size,
            'params': self.params
        }

    @staticmethod
    def from_config(config):
        if not config:
            return None

        config_dict = config.to_dict()
        config_dict = remove_empty_keys(config_dict)
        return Bridge.objects.create(**config_dict)

    def to_config(self):
        return plx.configs.SubGraphConfig(**self.to_dict())


class SubGraph(DiffModel):
    definition = models.TextField()

    def to_dict(self):
        return {'definition': self.definition}

    def __str__(self):
        return '{}'.format(self.id)

    @staticmethod
    def from_config(config):
        if not config:
            return None

        config_dict = config.to_dict()
        config_dict = remove_empty_keys(config_dict)
        return SubGraph.objects.create(definition=json.dumps(config_dict))

    def to_config(self):
        return plx.configs.SubGraphConfig.read_configs(json.loads(self.definition))


class Encoder(DiffModel):
    ENCODERS = ((obj, obj) for obj in plx.encoders.ENCODERS.keys())

    module = models.CharField(max_length=256, choices=ENCODERS, null=True, blank=True)
    definition = models.TextField()

    def __str__(self):
        return '{}-{}'.format(self.module, self.id)

    def to_dict(self):
        return {'module': self.module, 'definition': self.definition}

    @staticmethod
    def from_config(config):
        if not config:
            return None

        config_dict = config.to_dict()
        module = config_dict.pop('module', None)
        return Encoder.objects.create(module=module, definition=json.dumps(config_dict))

    def to_config(self):
        return plx.configs.SubGraphConfig.read_configs([{'module': self.module},
                                                        json.loads(self.definition)])


class Decoder(DiffModel):
    DECODERS = ((obj, obj) for obj in plx.decoders.DECODERS.keys())

    module = models.CharField(max_length=256, choices=DECODERS, null=True, blank=True)
    definition = models.TextField()

    def __str__(self):
        return '{}-{}'.format(self.module, self.id)

    def to_dict(self):
        return {'module': self.module, 'definition': self.definition}

    @staticmethod
    def from_config(config):
        if not config:
            return None

        config_dict = config.to_dict()
        module = config_dict.pop('module', None)
        return Decoder.objects.create(module=module, definition=json.dumps(config_dict))

    def to_config(self):
        return plx.configs.SubGraphConfig.read_configs([{'module': self.module},
                                                        json.loads(self.definition)])


class PolyaxonModel(DiffModel):
    MODELS = ((obj, obj) for obj in plx.models.MODELS.keys())
    SUMMARIES = ((obj, obj) for obj in SummaryOptions.VALUES)

    module = models.CharField(max_length=256, choices=MODELS)
    summaries = ArrayField(base_field=models.CharField(max_length=256, choices=SUMMARIES),
                           default=['all'])
    loss = models.ForeignKey(Loss, null=True, blank=True)
    eval_metrics = models.ManyToManyField(Metric)
    optimizer = models.ForeignKey(Optimizer, null=True, blank=True)
    graph = models.ForeignKey(SubGraph, null=True, blank=True)
    encoder = models.ForeignKey(Encoder, null=True, blank=True)
    decoder = models.ForeignKey(Decoder, null=True, blank=True)
    bridge = models.ForeignKey(Bridge, null=True, blank=True)
    clip_gradients = models.FloatField(default=5.0)
    clip_embed_gradients = models.FloatField(default=0.1)
    params = JSONField(blank=True, null=True, default={})

    def __str__(self):
        return '{}-{}'.format(self.module, self.id)

    def to_dict(self):
        return {
            'module': self.module,
            'summaries': self.summaries,
            'clip_gradients': self.clip_gradients,
            'clip_embed_gradients': self.clip_embed_gradients,
            'loss': self.loss.to_dict() if self.loss else None,
            'eval_metrics': [m.to_dict() for m in self.eval_metrics.all()],
            'optimizer': self.optimizer.to_dict() if self.optimizer else None,
            'graph': self.graph.to_dict() if self.graph else None,
            'encoder': self.encoder.to_dict() if self.encoder else None,
            'decoder': self.decoder.to_dict() if self.decoder else None,
            'bridge': self.bridge.to_dict() if self.bridge else None,
            'params': self.params,
        }

    @staticmethod
    def from_config(config):
        if not config:
            return None
        params = {}
        fields = [f.name for f in PolyaxonModel._meta.get_fields()]
        config_dict = config.to_dict()
        if not isinstance(config_dict.get('summaries', []), list):
            config_dict['summaries'] = [config_dict['summaries']]

        config_dict['params'] = params
        config_dict['loss'] = Loss.from_config(config.loss_config)
        config_dict.pop('loss_config', None)
        config_dict['optimizer'] = Optimizer.from_config(config.optimizer_config)
        config_dict.pop('optimizer_config', None)
        config_dict['graph'] = SubGraph.from_config(config.graph_config)
        config_dict.pop('graph_config', None)
        config_dict['encoder'] = Encoder.from_config(config.encoder_config)
        config_dict.pop('encoder_config', None)
        config_dict['decoder'] = Decoder.from_config(config.decoder_config)
        config_dict.pop('decoder_config', None)
        config_dict['bridge'] = Bridge.from_config(config.bridge_config)
        config_dict.pop('bridge_config', None)

        # also remove eval_metrics_config
        config_dict.pop('eval_metrics_config', None)

        # Rest of the keys should go to params
        keys = list(config_dict.keys())

        for key in keys:
            if key not in fields:
                params[key] = config_dict.pop(key)

        config_dict['params'] = params

        config_dict = remove_empty_keys(config_dict)
        model = PolyaxonModel.objects.create(**config_dict)
        model.eval_metrics = [Metric.from_config(m) for m in config.eval_metrics_config]
        return model

    def to_config(self):
        config_dict = {
            'module': self.module,
            'summaries': self.summaries,
            'clip_gradients': self.clip_gradients,
            'clip_embed_gradients': self.clip_embed_gradients,
            'loss_config': self.loss.to_config() if self.loss else None,
            'eval_metrics_config': [m.to_config() for m in self.eval_metrics.all()],
            'optimizer_config': self.optimizer.to_config() if self.optimizer else None,
            'graph_config': self.graph.to_config() if self.graph else None,
            'encoder_config': self.encoder.to_config() if self.encoder else None,
            'decoder_config': self.decoder.to_config() if self.decoder else None,
            'bridge_config': self.bridge.to_config() if self.bridge else None,
        }
        config_dict.update(self.params)
        return plx.configs.ModelConfig(**config_dict)


class Estimator(DiffModel):
    ESTIMATORS = ((obj, obj) for obj in plx.estimators.ESTIMATORS.keys())

    module = models.CharField(max_length=256, choices=ESTIMATORS)
    output_dir = models.CharField(max_length=256, blank=True, null=True)
    params = JSONField(blank=True, null=True, default={})

    def __str__(self):
        return '{}-{}'.format(self.module, self.id)

    def to_dict(self):
        return {'module': self.module, 'output_dir': self.output_dir, 'params': self.params}

    @staticmethod
    def from_config(config):
        if not config:
            return None

        config_dict = config.to_dict()
        config_dict = remove_empty_keys(config_dict)
        return Estimator.objects.create(**config_dict)

    def to_config(self):
        return plx.configs.EstimatorConfig(**self.to_dict())


class Agent(DiffModel):
    AGENTS = ((obj, obj) for obj in plx.estimators.AGENTS.keys())

    module = models.CharField(max_length=256, choices=AGENTS)
    memory = models.ForeignKey(AgentMemory)
    output_dir = models.CharField(max_length=256, blank=True, null=True)
    params = JSONField(blank=True, null=True, default={})

    def __str__(self):
        return '{}-{}'.format(self.module, self.id)

    def to_dict(self):
        return {'module': self.module,
                'memory': self.memory.to_dict(),
                'output_dir': self.output_dir,
                'params': self.params}

    @staticmethod
    def from_config(config):
        if not config:
            return None

        config_dict = config.to_dict()
        config_dict.pop('memory_config', None)
        config_dict['memory'] = AgentMemory.from_config(config.memory_config)
        config_dict = remove_empty_keys(config_dict)
        return Agent.objects.create(**config_dict)

    def to_config(self):
        config_dict = {
            'module': self.module,
            'memory_config': self.memory.to_config(),
            'output_dir': self.output_dir,
            'params': self.params}
        return plx.configs.EstimatorConfig(**config_dict)


class Environment(DiffModel):
    ENVIRONMENTS = ((obj, obj) for obj in plx.rl.environments.ENVIRONMENTS.keys())

    module = models.CharField(max_length=256, choices=ENVIRONMENTS)
    env_id = models.CharField(max_length=256)
    params = JSONField(blank=True, null=True, default={})

    def __str__(self):
        return '{}-{}'.format(self.module, self.id)

    def to_dict(self):
        return {'module': self.module, 'env_id': self.env_id, 'params': self.params}

    @staticmethod
    def from_config(config):
        if not config:
            return None

        config_dict = config.to_dict()
        config_dict = remove_empty_keys(config_dict)
        return Environment.objects.create(**config_dict)

    def to_config(self):
        return plx.configs.EnvironmentConfig(**self.to_dict())


class Pipeline(DiffModel):
    PIPELINES = ((obj, obj) for obj in plx.processing.pipelines.PIPELINES.keys())

    module = models.CharField(max_length=256, choices=PIPELINES, null=True, blank=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    definition = models.TextField()
    dynamic_pad = models.BooleanField(default=True)
    bucket_boundaries = models.BooleanField(default=False)
    batch_size = models.IntegerField(default=64)
    num_epochs = models.IntegerField(default=1)
    min_after_dequeue = models.IntegerField(default=5000)
    num_threads = models.IntegerField(default=3)
    shuffle = models.BooleanField(default=False)
    allow_smaller_final_batch = models.BooleanField(default=True)
    params = JSONField(blank=True, null=True, default={})

    def __str__(self):
        return ('{}-{}-{}'.format(self.module, self.name, self.id) if self.name
                else '{}-{}'.format(self.module, self.id))

    def to_dict(self):
        kwargs = {
            'module': self.module,
            'name': self.name,
            'definition': self.definition,
            'dynamic_pad': self.dynamic_pad,
            'bucket_boundaries': self.bucket_boundaries,
            'batch_size': self.batch_size,
            'num_epochs': self.num_epochs,
            'min_after_dequeue': self.min_after_dequeue,
            'num_threads': self.num_threads,
            'shuffle': self.shuffle,
            'allow_smaller_final_batch': self.allow_smaller_final_batch,
            'params': self.params
        }
        return kwargs

    @staticmethod
    def from_config(config):
        if not config:
            return None

        config_dict = config.to_dict()
        config_dict['definition'] = json.dumps(config_dict.get('definition', {}))
        config_dict = remove_empty_keys(config_dict)
        pipeline = Pipeline.objects.create(**config_dict)

        return pipeline

    def to_config(self):
        config_dict = self.to_dict()
        config_dict['definition'] = json.loads(config_dict.get('definition', {}))
        return plx.configs.PipelineConfig.read_configs(config_dict)


class InputData(DiffModel):
    INPUT_DATA_TYPES = (
        ('NUMPY', 'NUMPY'),
        ('PANDAS', 'PANDAS')
    )

    input_type = models.CharField(max_length=256, choices=INPUT_DATA_TYPES, blank=True, null=True)
    pipeline = models.ForeignKey(Pipeline)

    def __str__(self):
        return '{}-{}'.format(self.input_type, self.pipeline)

    def to_dict(self):
        return {
            'input_type': self.input_type,
            'pipeline': self.pipeline.to_dict()
        }

    @staticmethod
    def from_config(config):
        if not config:
            return None

        return InputData.objects.create(
            input_type=config.input_type,
            pipeline=Pipeline.from_config(config.pipeline_config))

    def to_config(self):
        return plx.configs.InputDataConfig(input_type=self.input_type,
                                           pipeline_config=self.pipeline.to_config())


class RunConfig(DiffModel):
    model_dir = models.CharField(max_length=256, blank=True, null=True)
    master = models.CharField(max_length=256, blank=True, null=True)
    num_cores = models.IntegerField(default=0)
    log_device_placement = models.BooleanField(default=False)
    gpu_memory_fraction = models.FloatField(default=1.0)
    tf_random_seed = models.IntegerField(blank=True, null=True)
    save_summary_steps = models.IntegerField(default=100, null=True, blank=True)
    save_checkpoints_secs = models.IntegerField(default=600, null=True, blank=True)
    save_checkpoints_steps = models.IntegerField(blank=True, null=True)
    keep_checkpoint_max = models.IntegerField(default=5, null=True, blank=True)
    keep_checkpoint_every_n_hours = models.IntegerField(default=10000, null=True, blank=True)
    evaluation_master = models.CharField(max_length=256, blank=True, null=True, default='')
    gpu_allow_growth = models.BooleanField(default=False)
    cluster_config = JSONField(blank=True, null=True, default={})

    def to_dict(self):
        return {
            'master': self.master,
            'num_cores': self.num_cores,
            'log_device_placement': self.log_device_placement,
            'gpu_memory_fraction': self.gpu_memory_fraction,
            'tf_random_seed': self.tf_random_seed,
            'save_summary_steps': self.save_summary_steps,
            'save_checkpoints_secs': self.save_checkpoints_secs,
            'save_checkpoints_steps': self.save_checkpoints_steps,
            'keep_checkpoint_max': self.keep_checkpoint_max,
            'keep_checkpoint_every_n_hours': self.keep_checkpoint_every_n_hours,
            'evaluation_master': self.evaluation_master,
            'gpu_allow_growth': self.gpu_allow_growth,
            'cluster_config': self.cluster_config
        }

    def __str__(self):
        return '{}'.format(self.id)

    @staticmethod
    def from_config(config):
        if not config:
            return None

        config_dict = config.to_dict()
        config_dict = remove_empty_keys(config_dict)
        return RunConfig.objects.create(**config_dict)

    def to_config(self):
        return plx.configs.RunConfig.read_configs(self.to_dict())


class BaseExperiment(DiffModel):
    HOOK_OPTIONS = ((obj, obj) for obj in HOOKS.keys())

    name = models.CharField(max_length=256)
    output_dir = models.CharField(max_length=256)
    run_config = models.ForeignKey(RunConfig)
    model = models.ForeignKey(PolyaxonModel)
    train_hooks = ArrayField(base_field=models.CharField(max_length=256, choices=HOOK_OPTIONS),
                             blank=True, null=True, default=[])
    eval_hooks = ArrayField(base_field=models.CharField(max_length=256, choices=HOOK_OPTIONS),
                            blank=True, null=True, default=[])
    eval_metrics = models.ManyToManyField(Metric, blank=True)
    eval_every_n_steps = models.IntegerField(default=1000)
    train_steps = models.IntegerField(default=10000)
    eval_steps = models.IntegerField(default=10)
    eval_delay_secs = models.IntegerField(default=0)
    continuous_eval_throttle_secs = models.IntegerField(default=60)
    delay_workers_by_global_step = models.BooleanField(default=False)
    export_strategies = models.CharField(max_length=256, blank=True, null=True)
    train_steps_per_iteration = models.IntegerField(default=1000)

    class Meta:
        abstract = True

    def __str__(self):
        return '{}-{}'.format(self.name, self.id)

    def to_dict(self):
        return {
            'name': self.name,
            'output_dir': self.output_dir,
            'run_config': self.run_config.to_dict(),
            'model': self.model.to_dict(),
            'train_hooks': self.train_hooks,
            'eval_hooks': self.eval_hooks,
            'eval_metrics': [m.to_dict() for m in self.eval_metrics.all()],
            'eval_every_n_steps': self.eval_every_n_steps,
            'train_steps': self.train_steps,
            'eval_steps': self.eval_steps,
            'eval_delay_secs': self.eval_delay_secs,
            'continuous_eval_throttle_secs': self.continuous_eval_throttle_secs,
            'delay_workers_by_global_step': self.delay_workers_by_global_step,
            'train_steps_per_iteration': self.train_steps_per_iteration
        }

    @staticmethod
    def from_config(config):
        config_dict = config.to_dict()
        config_dict['run_config'] = RunConfig.from_config(config.run_config)
        config_dict['model'] = PolyaxonModel.from_config(config.model_config)
        config_dict.pop('model_config', None)
        config_dict['eval_metrics'] = [Metric.from_config(m)
                                       for m in config.eval_metrics_config]
        config_dict.pop('eval_metrics_config', None)
        config_dict['train_hooks'] = config_dict.pop('train_hooks_config', [])
        config_dict['eval_hooks'] = config_dict.pop('eval_hooks_config', [])
        return config_dict

    def to_config(self):
        return {
            'name': self.name,
            'output_dir': self.output_dir,
            'run_config': self.run_config.to_config(),
            'model_config': self.model.to_config(),
            'train_hooks_config': self.train_hooks,
            'eval_hooks_config': self.eval_hooks,
            'eval_metrics_config': [m.to_config() for m in self.eval_metrics.all()],
            'eval_every_n_steps': self.eval_every_n_steps,
            'train_steps': self.train_steps,
            'eval_steps': self.eval_steps,
            'eval_delay_secs': self.eval_delay_secs,
            'continuous_eval_throttle_secs': self.continuous_eval_throttle_secs,
            'delay_workers_by_global_step': self.delay_workers_by_global_step,
            'train_steps_per_iteration': self.train_steps_per_iteration
        }


class Experiment(BaseExperiment):
    estimator = models.ForeignKey(Estimator)
    train_input_data = models.ForeignKey(InputData, related_name='train')
    eval_input_data = models.ForeignKey(InputData, related_name='eval')

    def to_dict(self):
        kwargs = super(Experiment, self).to_dict()
        kwargs['estimator'] = self.estimator.to_dict()
        kwargs['train_input_data'] = self.train_input_data.to_dict()
        kwargs['eval_input_data'] = self.eval_input_data.to_dict()

        return kwargs

    @staticmethod
    def from_config(config):
        config_dict = BaseExperiment.from_config(config)
        config_dict['estimator'] = Estimator.from_config(config.estimator_config)
        config_dict.pop('estimator_config', None)
        config_dict['train_input_data'] = InputData.from_config(config.train_input_data_config)
        config_dict.pop('train_input_data_config', None)
        config_dict['eval_input_data'] = InputData.from_config(config.eval_input_data_config)
        config_dict.pop('eval_input_data_config', None)
        eval_metrics = config_dict.pop('eval_metrics')

        config_dict = remove_empty_keys(config_dict)
        exp = Experiment.objects.create(**config_dict)
        exp.eval_metrics = eval_metrics
        return exp

    def to_config(self):
        to_config = super(Experiment, self).to_config()
        to_config['estimator_config'] = self.estimator.to_config()
        to_config['train_input_data_config'] = self.train_input_data.to_config()
        to_config['eval_input_data_config'] = self.eval_input_data.to_config()
        return plx.configs.ExperimentConfig(**to_config)


class RLExperiment(BaseExperiment):
    agent = models.ForeignKey(Agent)
    environment = models.ForeignKey(Environment)

    def to_dict(self):
        kwargs = super(RLExperiment, self).to_dict()
        kwargs['agent'] = self.estimator.to_dict()
        kwargs['env'] = self.env.to_dict()

        return kwargs

    @staticmethod
    def from_config(config):
        config_dict = BaseExperiment.from_config(config)
        config_dict['agent'] = Agent.from_config(config.agent_config)
        config_dict.pop('agent_config', None)
        config_dict['environment'] = Environment.from_config(config.environment_config)
        config_dict.pop('environment_config', None)
        eval_metrics = config_dict.pop('eval_metrics')

        config_dict = remove_empty_keys(config_dict)
        exp = RLExperiment.objects.create(**config_dict)
        exp.eval_metrics = eval_metrics
        return exp

    def to_config(self):
        to_config = super(RLExperiment, self).to_config()
        to_config['agent_config'] = self.agent.to_config()
        to_config['environment_config'] = self.environment.to_config()
        return plx.configs.RLExperimentConfig(**to_config)
