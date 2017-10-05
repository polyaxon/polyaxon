# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import tensorflow as tf

from polyaxon_schemas.eval import EvalConfig
from polyaxon_schemas.polyaxonfile.polyaxonfile import PolyaxonFile
from polyaxon_schemas.train import TrainConfig
from polyaxon_schemas.settings import ClusterConfig

from polyaxon.experiments import Experiment
from polyaxon import Modes, getters
from polyaxon.estimators.run_config import RunConfig, TaskType
from polyaxon.processing.input_data import create_input_data_fn

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


def _get_local_cluster(num_workers, num_ps):
    host = '127.0.0.1'
    master_port = 10000
    worker_port = 11000
    ps_port = 12000

    def get_address(port):
        return '{}:{}'.format(host, port)

    cluster_config = {
        TaskType.MASTER: [get_address(master_port)]
    }

    workers = []
    for i in range(num_workers):
        workers.append(get_address(worker_port))
        worker_port += 1

    cluster_config[TaskType.WORKER] = workers

    ps = []
    for i in range(num_ps):
        ps.append(get_address(ps_port))
        ps_port += 1

    cluster_config[TaskType.PS] = ps

    return ClusterConfig.from_dict(cluster_config)


def _get_run_configs(polyaxonfile, experiment_id):
    plx_file = PolyaxonFile.read(polyaxonfile)
    environment = plx_file.get_environment_at(experiment_id)
    cluster_def, is_distributed = plx_file.get_cluster_def_at(experiment_id)

    def get_master_config(config, task_type=None, task_id=None):
        config = RunConfig.from_config(config)
        if task_type is None and task_id is None:
            return config
        return config.replace(task_type=task_type, task_id=task_id)

    config = environment.run_config or RunConfig.CONFIG()

    if not is_distributed:
        return {TaskType.MASTER: get_master_config(config)}, False

    config.cluster = plx_file.get_cluster(experiment=experiment_id)

    configs = {TaskType.MASTER: [get_master_config(config, TaskType.MASTER, 0)]}

    if cluster_def.get(TaskType.WORKER, 0) > 0:
        configs[TaskType.WORKER] = []

    if cluster_def.get(TaskType.PS, 0) > 0:
        configs[TaskType.PS] = []

    worker_session_configs = {}
    for session_config in environment.worker_configs or []:
        worker_session_configs[session_config.index] = session_config

    ps_session_configs = {}
    for session_config in environment.ps_configs or []:
        ps_session_configs[session_config.index] = session_config

    default_worker_config = environment.default_worker_config
    for i in range(cluster_def.get(TaskType.WORKER, 0)):
        w_config = get_master_config(config, task_type=TaskType.WORKER, task_id=i)
        session_config = worker_session_configs.get(i, default_worker_config)
        if session_config:
            session_config = RunConfig.get_session_config(session_config)
            w_config = w_config.replace(session_config=session_config)

        configs[TaskType.WORKER].append(w_config)

    default_ps_config = environment.default_ps_config
    for i in range(cluster_def.get(TaskType.PS, 0)):
        ps_config = get_master_config(config, task_type=TaskType.PS, task_id=i)
        session_config = ps_session_configs.get(i, default_ps_config)
        if session_config:
            session_config = RunConfig.get_session_config(session_config)
            ps_config = ps_config.replace(session_config=session_config)

        configs[TaskType.PS].append(ps_config)

    return configs, True


def prepare_experiment_run(polyaxonfile, experiment_id, task_type=TaskType.MASTER, task_id=0):
    plx_file = PolyaxonFile.read(polyaxonfile)
    cluster, is_distributed = plx_file.get_cluster_def_at(experiment_id)

    if (task_type not in cluster or
            not isinstance(cluster[task_type], int) or
            task_id >= cluster[task_type]):
        raise ValueError('task_type, task_id `{}, {}` is not supported by '
                         'the specification file passed.'.format(task_type, task_id))

    env = plx_file.get_environment_at(experiment_id)
    if not env:
        tf.logging.set_verbosity(tf.logging.INFO)
        configs = {TaskType.MASTER: [RunConfig()]}
        delay_workers_by_global_step = False
    else:
        tf.logging.set_verbosity(LOGGING_LEVEL[plx_file.settings.logging.level])
        configs, is_distributed = _get_run_configs(plx_file, experiment_id)
        delay_workers_by_global_step = env.delay_workers_by_global_step

    train_input_fn, train_steps, train_hooks = _get_train(plx_file.get_train_at(experiment_id))
    (eval_input_fn, eval_steps, eval_hooks, eval_delay_secs,
     continuous_eval_throttle_secs) = _get_eval(plx_file.get_eval_at(experiment_id))

    estimator = getters.get_estimator(plx_file.get_model_at(experiment_id),
                                      configs[task_type][task_id],
                                      output_dir=plx_file.get_project_path_at(experiment_id))

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
        export_strategies=plx_file.settings.export_strategies)


def prepare_all_experiment_runs(polyaxonfile):
    plx_file = PolyaxonFile.read(polyaxonfile)
    is_distributed = False

    if not plx_file.settings.environment:
        tf.logging.set_verbosity(tf.logging.INFO)
        configs = {TaskType.MASTER: [RunConfig()]}
        delay_workers_by_global_step = False
    else:
        tf.logging.set_verbosity(LOGGING_LEVEL[plx_file.settings.logging.level])
        configs, is_distributed = _get_run_configs(plx_file.settings.environment)
        delay_workers_by_global_step = plx_file.settings.environment.delay_workers_by_global_step

    train_input_fn, train_steps, train_hooks = _get_train(plx_file.train)
    (eval_input_fn, eval_steps, eval_hooks, eval_delay_secs,
     continuous_eval_throttle_secs) = _get_eval(plx_file.eval)

    def get_experiment(config):
        estimator = getters.get_estimator(plx_file.model,
                                          config,
                                          output_dir=plx_file.project_path)

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
            export_strategies=plx_file.settings.export_strategies)

    xps = [get_experiment(configs[TaskType.MASTER][0])]
    if not is_distributed:
        return xps

    for i_config in configs.get(TaskType.WORKER, []):
        xps.append(get_experiment(i_config))

    for i_config in configs.get(TaskType.PS, []):
        xps.append(get_experiment(i_config))

    return xps
