# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import os
import tensorflow as tf

from polyaxon_schemas.eval import EvalConfig
from polyaxon_schemas.polyaxonfile.specification import Specification
from polyaxon_schemas.settings import ClusterConfig
from polyaxon_schemas.train import TrainConfig
from polyaxon_schemas.utils import TaskType

from polyaxon.experiments import Experiment
from polyaxon import Modes, getters
from polyaxon.estimators.run_config import RunConfig
from polyaxon.processing.input_data import create_input_data_fn
from polyaxon.polyaxonfile import constants

LOGGING_LEVEL = {
    'INFO': tf.logging.INFO,
    'DEBUG': tf.logging.DEBUG,
    'WARN': tf.logging.WARN,
    'ERROR': tf.logging.ERROR,
    'FATAL': tf.logging.FATAL,
}


def _get_train(config):
    assert isinstance(config, TrainConfig), '`config` must be a an instance of `TrainConfig`'

    input_fn = create_input_data_fn(
        mode=Modes.TRAIN,
        pipeline_config=config.data_pipeline
    )
    return input_fn, config.steps, config.hooks


def _get_eval(config):
    assert isinstance(config, EvalConfig), '`config` must be a an instance of `EvalConfig`'

    input_fn = create_input_data_fn(
        mode=Modes.EVAL,
        pipeline_config=config.data_pipeline
    )
    return (input_fn,
            config.steps,
            config.hooks,
            config.delay_secs,
            config.continuous_eval_throttle_secs)


def _get_run_configs(spec_config, experiment_uuid):
    spec = Specification.read(spec_config)
    environment = spec.environment
    cluster_def, is_distributed = spec.cluster_def

    def get_master_config(config, task_type=None, task_id=None):
        config = RunConfig.from_config(config)
        if task_type is None and task_id is None:
            return config
        return config.replace(task_type=task_type, task_id=task_id)

    config = environment.run_config or RunConfig.CONFIG()

    if not is_distributed:
        return {TaskType.MASTER: [get_master_config(config)]}, False

    if spec.is_local:
        config.cluster = spec.get_local_cluster()
    else:
        # Get value from env
        master = os.getenv(constants.CLUSTER_CONFIG_MAP_KEY_NAME.format(
            experiment_uuid=experiment_uuid, task_type=TaskType.MASTER), '')
        worker = os.getenv(constants.CLUSTER_CONFIG_MAP_KEY_NAME.format(
            experiment_uuid=experiment_uuid, task_type=TaskType.WORKER), '')
        ps = os.getenv(constants.CLUSTER_CONFIG_MAP_KEY_NAME.format(
            experiment_uuid=experiment_uuid, task_type=TaskType.PS), '')
        cluster_dict = {
            TaskType.MASTER: master,
            TaskType.WORKER: worker,
            TaskType.PS: ps
        }
        config.cluster = ClusterConfig.from_dict(cluster_dict)

    configs = {TaskType.MASTER: [get_master_config(config, TaskType.MASTER, 0)]}

    if cluster_def.get(TaskType.WORKER, 0) > 0:
        configs[TaskType.WORKER] = []

    if cluster_def.get(TaskType.PS, 0) > 0:
        configs[TaskType.PS] = []

    worker_session_configs = spec.worker_configs
    ps_session_configs = spec.ps_configs

    for i in range(cluster_def.get(TaskType.WORKER, 0)):
        w_config = get_master_config(config, task_type=TaskType.WORKER, task_id=i)
        session_config = worker_session_configs.get(i)
        if session_config:
            session_config = RunConfig.get_session_config(session_config)
            w_config = w_config.replace(session_config=session_config)

        configs[TaskType.WORKER].append(w_config)

    for i in range(cluster_def.get(TaskType.PS, 0)):
        ps_config = get_master_config(config, task_type=TaskType.PS, task_id=i)
        session_config = ps_session_configs.get(i)
        if session_config:
            session_config = RunConfig.get_session_config(session_config)
            ps_config = ps_config.replace(session_config=session_config)

        configs[TaskType.PS].append(ps_config)

    return configs, True


def prepare_experiment_run(spec_config, experiment_uuid, task_type=TaskType.MASTER, task_id=0):
    spec = Specification.read(spec_config)
    cluster, _ = spec.cluster_def

    if (task_type not in cluster or
            not isinstance(cluster[task_type], int) or
                task_id >= cluster[task_type]):
        raise ValueError('task_type, task_id `{}, {}` is not supported by '
                         'the specification file passed.'.format(task_type, task_id))

    env = spec.environment
    if not env:
        tf.logging.set_verbosity(tf.logging.INFO)
        configs = {TaskType.MASTER: [RunConfig()]}
        delay_workers_by_global_step = False
    else:
        tf.logging.set_verbosity(LOGGING_LEVEL[spec.settings.logging.level])
        configs, _ = _get_run_configs(spec, experiment_uuid)
        delay_workers_by_global_step = env.delay_workers_by_global_step

    train_input_fn, train_steps, train_hooks = _get_train(spec.train)
    (eval_input_fn, eval_steps, eval_hooks, eval_delay_secs,
     continuous_eval_throttle_secs) = _get_eval(spec.eval)

    estimator = getters.get_estimator(spec.model,
                                      configs[task_type][task_id],
                                      output_dir=spec.project_path)

    return Experiment(
        estimator=estimator,
        train_input_fn=train_input_fn,
        eval_input_fn=eval_input_fn,
        train_steps=train_steps,
        eval_steps=eval_steps,
        train_hooks=train_hooks,
        eval_hooks=eval_hooks,
        eval_delay_secs=eval_delay_secs,
        continuous_eval_throttle_secs=continuous_eval_throttle_secs,
        delay_workers_by_global_step=delay_workers_by_global_step,
        export_strategies=spec.settings.export_strategies)


def start_experiment_run(spec_config, experiment_uuid, task_type, task_id, schedule):
    spec = Specification.read(spec_config)
    experiment = prepare_experiment_run(spec, experiment_uuid, task_type, int(task_id))
    task = getattr(experiment, schedule)
    return task()


def prepare_all_experiment_jobs(spec_config, experiment_uuid):
    spec = Specification.read(spec_config)
    is_distributed = False

    if not spec.environment:
        tf.logging.set_verbosity(tf.logging.INFO)
        configs = {TaskType.MASTER: [RunConfig()]}
        delay_workers_by_global_step = False
    else:
        tf.logging.set_verbosity(LOGGING_LEVEL[spec.settings.logging.level])
        configs, is_distributed = _get_run_configs(spec, experiment_uuid)
        delay_workers_by_global_step = spec.environment.delay_workers_by_global_step

    train_input_fn, train_steps, train_hooks = _get_train(spec.train)
    (eval_input_fn, eval_steps, eval_hooks, eval_delay_secs,
     continuous_eval_throttle_secs) = _get_eval(spec.eval)

    def get_experiment(config):
        estimator = getters.get_estimator(spec.model,
                                          config,
                                          output_dir=spec.project_path)

        return Experiment(
            estimator=estimator,
            train_input_fn=train_input_fn,
            eval_input_fn=eval_input_fn,
            train_steps=train_steps,
            eval_steps=eval_steps,
            train_hooks=train_hooks,
            eval_hooks=eval_hooks,
            eval_delay_secs=eval_delay_secs,
            continuous_eval_throttle_secs=continuous_eval_throttle_secs,
            delay_workers_by_global_step=delay_workers_by_global_step,
            export_strategies=spec.settings.export_strategies)

    xps = [get_experiment(configs[TaskType.MASTER][0])]
    if not is_distributed:
        return xps

    for i_config in configs.get(TaskType.WORKER, []):
        xps.append(get_experiment(i_config))

    for i_config in configs.get(TaskType.PS, []):
        xps.append(get_experiment(i_config))

    return xps
